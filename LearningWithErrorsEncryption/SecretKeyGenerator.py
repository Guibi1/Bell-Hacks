import random
from sympy.ntheory.factor_ import totient
import numpy as np

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


    totient_sum = totient(total_sum)
    key = (closest_prime_of_smallest*closest_prime) + totient_sum*largest_num

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

def encryptedlisttoarray(input, publickey):
    width = publickey.shape[1]-1
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output

chosen_words = words_to_list('LearningWithErrorsEncryption\words300.txt')
four_selected_words = pick_four_words(chosen_words)
secret_key = hash_words(four_selected_words)
public_key = generate_public_key(secret_key, 20, random.choice(prime_list_larger_100))
message = "helpmeiwanttodie"
encryptedmessage = encryptstring(message,public_key)
outputencrypted = encryptedarraytolist(encryptedmessage)
decryptedmessage = decryptstring(encryptedmessage,secret_key,public_key)
unflattened = encryptedlisttoarray(outputencrypted,public_key)

print("Randomly selected words: \n", four_selected_words)
print("Secret key: \n", secret_key)
print("Public Key: \n", public_key[:,0:public_key.shape[1]-1])
print("Message: \n", message)
print("Encrypted Message: \n",encryptedmessage)
print("Flattened Encrypted Message: \n", outputencrypted)
print("Unflattened Encrypted Message: \n", unflattened)

print("Decrypted Message: \n",decryptedmessage)

