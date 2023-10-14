

from http.server import BaseHTTPRequestHandler
import random
import numpy as np
import json

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]
prime_list_larger_100 = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]

def words_to_list(input_file):
    word_list = []
    with open(input_file, 'r') as file:
        for line in file:
            words = line.split()
            word_list.extend(words)
    return word_list

def find_closest_prime(target, prime_list):
    closest_prime = None
    min_difference = float('inf')

    for prime in prime_list:
        difference = abs(target - prime)
        if difference < min_difference:
            min_difference = difference
            closest_prime = prime

    return closest_prime

def pick_four_words(word_list):
    selected_words = random.sample(word_list, 4)
    return selected_words

def hash_function(word):
    word = word.lower()
    total_sum = 0
    smallest_num = 100
    second_smallest_num = 100
    largest_num = 0
    current_char = 1
    for char in word:
        char_num = ord(char) - 96
        total_sum += char_num*current_char
        current_char+=1
        if char_num < smallest_num:
            smallest_num = char_num
        elif char_num < second_smallest_num:
            second_smallest_num = char_num

        if char_num > smallest_num:
            largest_num = char_num
        

    sum_smallest = smallest_num + second_smallest_num
    closest_prime = find_closest_prime(total_sum, prime_list)
    closest_prime_of_smallest = find_closest_prime(sum_smallest, prime_list)


    key = (closest_prime_of_smallest*closest_prime)+largest_num

    return key

def hash_words(selected_words):
    encrypted_words = [hash_function(word) for word in selected_words]
    return encrypted_words

def generate_public_key(secretkey, publickeycount, modulus):

    vectorsize = len(secretkey)

    publickey = np.random.randint(100, 400, (publickeycount, vectorsize))

    publickeysecretkeymult = publickey * secretkey

    publickeysecretkeymultsum = publickeysecretkeymult.sum(axis=1)

    noise = np.random.randint(-4, 4, publickeycount)

    addednoise = np.add(noise, publickeysecretkeymultsum)

    addedmodulus = addednoise % modulus

    finalpublickey = np.column_stack((publickey, addedmodulus))
    
    finalpublickey = np.column_stack((finalpublickey,np.ones([publickeycount,1])*modulus))
    
    return finalpublickey

def encryptdata(input, inputpublickey):

    encryptedarray = []
    inputmodulus = int(inputpublickey[0,inputpublickey.shape[1]-1])
    binary_representation = np.binary_repr(input)
    bits = np.array([int(bit) for bit in binary_representation], dtype=int)
    pk = inputpublickey[:,:inputpublickey.shape[1]-2]
    pkr = inputpublickey[:,inputpublickey.shape[1]-2:inputpublickey.shape[1]-1]
    i = 0
    while (i < bits.shape[0]):
        currentbit = bits[i]
        randpublickeys = np.random.randint(0,inputpublickey.shape[0]-1,5)
        u = (pk[randpublickeys[0]] + pk[randpublickeys[1]] + pk[randpublickeys[2]]+pk[randpublickeys[3]]+pk[randpublickeys[4]]).__mod__(inputmodulus)
        v = ((pkr[randpublickeys[0]] + pkr[randpublickeys[1]] + pkr[randpublickeys[2]]+pkr[randpublickeys[3]]+pkr[randpublickeys[4]]) + int(inputmodulus/2)*currentbit).__mod__(inputmodulus)
        
        appended = np.append(u,v)
        encryptedarray.append(appended)
        i+=1
    
    encryptedarray = np.array(encryptedarray)
    return encryptedarray

def decryptdata(input, inputsecretkey, publickey):
    decryptarray = []
    inputmodulus = publickey[0,publickey.shape[1]-1]
    
    u = input[:,:input.shape[1]-1]
    v = input[:,input.shape[1]-1]
    i = 0
    halfmod = int(inputmodulus/2)
    while (i < len(input)):
        
        dec = (v[i] - np.matmul(inputsecretkey,u[i])).__mod__(inputmodulus)
        if (((inputmodulus - dec) < abs(halfmod-dec)) or ((dec) < abs(halfmod-dec))): 
            val = 0
        else:
            val = 1
        decryptarray.append(val)
        i+=1    

    return decryptarray

def encryptbyte(input, inputpublickey):

    encryptedarray = []
    inputmodulus = int(inputpublickey[0,inputpublickey.shape[1]-1])
    binary_representation = input
    bits = np.array([int(bit) for bit in binary_representation], dtype=int)
    pk = inputpublickey[:,:inputpublickey.shape[1]-2]
    pkr = inputpublickey[:,inputpublickey.shape[1]-2:inputpublickey.shape[1]-1]
    i = 0
    while (i < bits.shape[0]):

        currentbit = bits[i]
        randpublickeys = np.random.randint(0,inputpublickey.shape[0]-1,5)
        u = (pk[randpublickeys[0]] + pk[randpublickeys[1]] + pk[randpublickeys[2]]+pk[randpublickeys[3]]+pk[randpublickeys[4]]).__mod__(inputmodulus)
        v = ((pkr[randpublickeys[0]] + pkr[randpublickeys[1]] + pkr[randpublickeys[2]]+pkr[randpublickeys[3]]+pkr[randpublickeys[4]]) + int(inputmodulus/2)*currentbit).__mod__(inputmodulus)
        
        appended = np.append(u,v)
        encryptedarray.append(appended)
        i+=1
    
    encryptedarray = np.array(encryptedarray)
    return encryptedarray

def encryptcharacter(input, inputpublickey):
    char_num = ord(input)
    char_bin = np.binary_repr(char_num,8)
    encrypted_byte = encryptbyte(char_bin,inputpublickey)
    return encrypted_byte

def encryptstring(input, inputpublickey):
    input = str(input)
    encryptedarray = np.empty(shape=[0,5])
    for chars in input:
        encryptedchar = encryptcharacter(chars,inputpublickey)
        encryptedarray = np.vstack((encryptedarray,encryptedchar))
    
    return encryptedarray

def decryptstring(input, inputsecretkey, publickey):
    
    bit_array = np.array(decryptdata(input, inputsecretkey, publickey))
    output = ""
    bitcount = bit_array.shape[0]/8
    i = 0
    while i < bitcount:
        currentbit = bit_array[0+i*8:8+i*8]
        decimal_number = int("".join(map(str, currentbit)), 2)
        currentchar = chr(decimal_number)
        output+=currentchar
        i+=1

    return output

def encryptedarraytolist(input):
    
    flattened = [element for row in input for element in row]
    return flattened

def publickeyarraytolist(input):
    
    flattened = [element for row in input for element in row]
    return flattened

def encryptedlisttoarray(input, publickey):
    width = publickey.shape[1]-1
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output

def publickeylisttoarray(input):
    width = 6
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output

def verifySecretKey(secretkey, publickey):
    if (len(secretkey) == 4): 
        publickeyarr = publickeylisttoarray(publickey)
        secretkeyarr = hash_words(secretkey)
        testmessage = str(random.randint(256,512))
        if (testmessage == decryptstring((encryptstring(testmessage,publickeyarr)),secretkeyarr,publickeyarr)):
            return True
        else: 
            return False
    else:
        return False

def publicKeyApiGenerator(secretkey):

    secretkeyarr = hash_words(secretkey)
    publickey = generate_public_key(secretkeyarr,20, random.choice(prime_list_larger_100))
    return np.array(publickeyarraytolist(publickey)).astype(int).tolist()

def encryptPasswordApi(password,publickeyinput):
    publickey = publickeylisttoarray(publickeyinput)
    encryptedpassword = encryptstring(password,publickey)
    return (np.array(encryptedarraytolist(encryptedpassword)).astype(int)).tolist()

def decryptPasswordApi(encryptedpassword, secretkeyinput, publickeyinput):
    publickey = publickeylisttoarray(publickeyinput)
    secretkey = hash_words(secretkeyinput)
    passwordarray = encryptedlisttoarray(encryptedpassword,publickey)
    password = decryptstring(passwordarray,secretkey,publickey)  
    return password


secret_key = [ "study", "entry", "thing", "portal" ]

public_key = [158, 157, 249, 268, 7, 179, 364, 396, 101, 158, 17, 179, 324, 231, 392, 198, 103, 179, 196, 280, 191, 174, 167, 179, 247, 104, 188, 255, 42, 179, 252, 217, 294, 208, 177, 179, 240, 242, 115, 374, 166, 179, 181, 253, 386, 172, 134, 179, 305, 164, 379, 362, 100, 179, 293, 199, 164, 370, 140, 179, 354, 104, 144, 128, 115, 179, 168, 276, 155, 219, 144, 179, 320, 327, 243, 312, 151, 179, 348, 281, 179, 265, 144, 179, 313, 258, 137, 370, 89, 179, 344, 271, 394, 110, 94, 179, 138, 239, 179, 166, 106, 179, 253, 293, 194, 333, 29, 179, 140, 203, 361, 215, 49, 179, 109, 210, 272, 171, 151, 179]

encrypt = [35, 25, 90, 1, 33, 46, 157, 37, 58, 74, 145, 141, 10, 72, 155, 60, 170, 5, 60, 135, 138, 136, 4, 18, 120, 127, 40, 100, 119, 165, 49, 168, 127, 162, 80, 79, 9, 16, 67, 171, 61, 136, 56, 169, 28, 137, 83, 171, 51, 68, 74, 80, 94, 16, 155, 32, 176, 134, 67, 105, 45, 64, 169, 94, 97, 42, 162, 88, 76, 75, 106, 173, 76, 113, 143, 57, 75, 150, 54, 20, 67, 68, 100, 26, 65, 12, 88, 23, 47, 105, 129, 156, 126, 65, 65, 150, 70, 80, 103, 167, 123, 49, 7, 79, 113, 140, 130, 13, 54, 87, 99, 86, 26, 38, 122, 80, 178, 82, 168, 156, 40, 127, 12, 0, 88, 0, 143, 158, 27, 174, 44, 89, 10, 167, 177, 58, 81, 79, 53, 135, 29, 142, 26, 69, 4, 110, 123, 78, 42, 67, 66, 64, 150, 131, 76, 170, 58, 18, 103, 76, 69, 142, 102, 171, 15, 113, 72, 23, 73, 36, 72, 135, 56, 47, 76, 20, 110, 80, 100, 177, 176, 151, 153, 95, 163, 142, 116, 65, 157, 109, 152, 111, 3, 76, 107, 15, 40, 111, 101, 105, 75, 28, 119, 17, 102, 47, 139, 163, 59, 20, 95, 52, 178, 135, 133, 33, 70, 68, 168, 137, 16, 7, 107, 148, 62, 146, 150, 4, 22, 176, 44, 48, 91, 26, 117, 76, 142, 76, 32, 146, 14, 69, 25, 79, 148, 128, 47, 140, 121, 129, 22, 33, 27, 92, 64, 177, 65, 137, 26, 175, 59, 36, 67, 88, 94, 116, 114, 22, 51, 103, 84, 13, 1, 130, 42, 126, 21, 22, 31, 166, 129, 5, 129, 83, 130, 166, 99, 115, 72, 121, 0, 42, 83, 63, 75, 38, 89, 46, 159, 75, 166, 4, 157, 166, 39, 106, 52, 22, 58, 3, 47, 59, 159, 42, 99, 155, 84, 101, 49, 0, 54, 27, 58, 151, 101, 0, 116, 40, 113, 152, 98, 114, 55, 111, 28, 51, 171, 143, 86, 43, 163, 92, 112, 127, 145, 48, 33, 62, 94, 94, 53, 45, 158, 138, 25, 6, 105, 137, 42, 103, 21, 159, 108, 96, 123, 144, 80, 32, 176, 87, 164, 41, 158, 161, 41, 44, 40, 36, 9, 159, 124, 21, 95, 27, 14, 27, 171, 101, 8, 21, 23, 115, 20, 30, 48, 114, 50, 156, 4, 170, 84, 75, 73, 79, 169, 121, 23, 110, 163, 0, 99, 26, 54, 169, 88, 177, 84, 157, 145, 145, 6, 127, 116, 163, 124, 100, 96, 77, 65, 120, 151, 81, 126, 96, 113, 80, 81, 83, 68, 6, 170, 137, 113, 132, 93, 19, 111, 141, 3, 61, 31, 137, 110, 32, 81, 107, 78, 103, 66, 119, 170, 92, 123, 113, 59, 112, 59, 74, 69, 171, 76, 152, 1, 114, 25, 27, 41, 61, 9, 39]
print(decryptPasswordApi(encrypt,secret_key,public_key))