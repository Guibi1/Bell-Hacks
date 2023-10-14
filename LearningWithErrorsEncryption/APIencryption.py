

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


secret_key = ["Voiture","Lover","Piscine","Chien"]

public_key = [291, 325, 125, 289, 95, 193, 386, 116, 184, 170, 1, 193, 336, 309, 348, 273, 159, 193, 141, 225, 295, 323, 147, 193, 169, 342, 284, 243, 100, 193, 353, 232, 186, 396, 77, 193, 148, 115, 138, 361, 181, 193, 190, 211, 336, 286, 68, 193, 203, 252, 189, 238, 121, 193, 198, 215, 263, 339, 111, 193, 194, 238, 182, 166, 96, 193, 128, 102, 340, 164, 109, 193, 297, 182, 136, 105, 102, 193, 177, 306, 265, 103, 95, 193, 380, 386, 145, 111, 191, 193, 230, 246, 338, 298, 11, 193, 181, 108, 264, 104, 41, 193, 353, 133, 284, 186, 44, 193, 183, 367, 195, 346, 141, 193, 388, 374, 176, 293, 102, 193]

encrypt =  [149, 114, 22, 3, 59, 152, 88, 147, 67, 182, 125, 188, 45, 97, 10, 54, 15, 108, 146, 112, 57, 75, 28, 13, 69, 192, 130, 133, 74, 11, 6, 36, 145, 44, 13, 45, 160, 0, 175, 68, 14, 93, 14, 82, 16, 174, 131, 108, 103, 42, 52, 42, 86, 85, 155, 49, 52, 187, 71, 134, 112, 41, 127, 166, 83, 100, 166, 12, 110, 181, 75, 105, 136, 40, 150, 157, 152, 144, 20, 91, 158, 90, 108, 192, 63, 0, 139, 136, 130, 164, 36, 110, 190, 168, 2, 67, 172, 14, 79, 130, 83, 55, 157, 159, 9, 79, 101, 17, 89, 157, 13, 32, 186, 172, 179, 89, 115, 185, 39, 92, 30, 116, 159, 144, 148, 33, 46, 116, 177, 174, 70, 154, 185, 114, 150, 116, 54, 74, 131, 95, 66, 73, 84, 185, 39, 186, 161, 9, 14, 102, 11, 9, 40, 149, 35, 177, 61, 115, 167, 34, 87, 79, 26, 90, 47, 16, 179, 75, 113, 63, 52, 55, 15, 172, 120, 158, 157, 104, 65, 2, 112, 122, 1, 160, 101, 62, 41, 115, 1, 191, 102, 175, 96, 184, 86, 121, 60, 116, 50, 112, 84, 48, 150, 104, 48, 105, 114, 1, 18, 151, 8, 114, 3, 112, 140, 176, 3, 23, 101, 172, 173, 26, 9, 174, 103, 164, 71, 87, 4, 19, 77, 65, 2, 133, 74, 3, 18, 162, 22, 109, 31, 85, 52, 5, 32, 109, 9, 22, 186, 84, 51, 14, 37, 188, 99, 118, 22, 164, 89, 36, 23, 153, 175, 125, 141, 152, 137, 159, 99, 133, 66, 129, 149, 87, 4, 6, 130, 50, 27, 173, 54, 145, 187, 123, 92, 3, 122, 116, 55, 149, 172, 100, 17, 154, 102, 26, 92, 117, 11, 13, 78, 15, 158, 110, 65, 139, 120, 0, 118, 112, 74, 26, 23, 73, 60, 16, 141, 168, 160, 133, 32, 111, 38, 192, 148, 88, 172, 49, 171, 173, 31, 31, 9, 93, 124, 83, 30, 43, 174, 91, 181, 174, 74, 89, 147, 26, 52, 187, 136, 53, 53, 39, 191, 111, 187, 154, 122, 110, 59, 181, 89, 74, 66, 84, 103, 157, 16, 170, 79, 27, 145, 124, 180, 109, 162, 1, 142, 150, 10, 152, 151, 175, 86, 162, 37, 118, 110, 26, 5, 1, 26, 134, 179, 182, 144, 188, 159, 61, 88, 32, 11, 48, 36, 110, 62, 35, 188, 137, 50, 96, 70, 158, 119, 14, 50, 99, 43, 36, 19, 57, 134, 130, 90, 49, 119, 128, 150, 80, 42, 178, 111, 157, 52, 68, 83, 61, 131, 181, 103, 154]

print(decryptPasswordApi(encrypt,secret_key,public_key))