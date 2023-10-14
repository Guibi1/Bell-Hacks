

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


secretkey = ["Voiture","Lover","Piscine","Chien"]
encryptedpasscode = [46, 175, 42, 21, 164, 80, 220, 301, 377, 185, 312, 375, 438, 78, 344, 229, 402, 248, 359, 123, 435, 439, 146, 269, 111, 285, 33, 340, 283, 213, 135, 157, 298, 233, 179, 135, 367, 47, 141, 144, 71, 400, 358, 233, 305, 309, 75, 110, 224, 73, 174, 167, 51, 410, 97, 243, 120, 344, 154, 34, 111, 29, 432, 306, 31, 429, 318, 316, 403, 445, 195, 431, 182, 102, 382, 22, 363, 194, 383, 428, 90, 313, 51, 159, 344, 386, 66, 328, 454, 17, 184, 389, 409, 299, 87, 68, 453, 273, 159, 147, 284, 106, 13, 148, 412, 62, 232, 12, 390, 321, 386, 445, 384, 64, 44, 335, 27, 340, 357, 259, 244, 278, 361, 117, 361, 135, 297, 46, 301, 117, 420, 138, 397, 268, 32, 295, 211, 337, 360, 19, 234, 309, 350, 21, 252, 167, 43, 348, 206, 260, 307, 204, 426, 326, 29, 283, 123, 254, 242, 411, 11, 167, 448, 54, 117, 69, 294, 94, 220, 46, 130, 421, 259, 331, 182, 447, 172, 434, 13, 22, 164, 451, 395, 405, 118, 404, 86, 355, 154, 347, 137, 120, 258, 234, 232, 372, 363, 357, 449, 60, 24, 129, 213, 10, 325, 368, 90, 380, 5, 121, 35, 152, 202, 126, 260, 415, 344, 54, 441, 38, 342, 191, 34, 391, 420, 189, 41, 152, 203, 451, 360, 179, 404, 296, 297, 52, 26, 46, 326, 396, 343, 314, 142, 304, 363, 302, 18, 284, 351, 175, 386, 140, 327, 338, 436, 74, 242, 228, 297, 59, 270, 435, 397, 446, 311, 310, 294, 390, 202, 203, 225, 347, 2, 191, 366, 361, 433, 425, 4, 159, 229, 6, 64, 310, 398, 25, 347, 309, 299, 149, 255, 85, 233, 291, 172, 113, 292, 354, 139, 236, 289, 208, 392, 416, 416, 332, 358, 443, 353, 244, 9, 74, 377, 362, 151, 4, 255, 248, 359, 9, 82, 228, 28, 83, 98, 61, 84, 363, 264, 165, 92, 206, 427, 394, 57, 64, 41, 423, 300, 53, 149, 228, 383, 51, 440, 223, 189, 400, 453, 245, 14, 65, 231, 139, 23, 262, 30, 352, 193, 121, 164, 192, 314, 376, 382, 165, 226, 210, 63, 266, 124, 30, 37, 424, 299, 243, 428, 224, 19, 344, 297, 215, 282, 2, 358, 423, 193, 416, 201, 114, 37, 306, 272, 153, 82, 61, 290, 24, 159, 281, 431, 61, 365, 366, 26, 354, 134, 371, 429, 408, 395, 243, 165, 94, 197, 423, 396, 240, 424, 421, 132, 203, 2, 413, 396, 411, 280, 30, 266, 178, 219, 193, 432, 296, 406, 451, 91, 362, 340, 14]
publickey = [213, 364, 189, 291, 294, 457, 308, 257, 235, 193, 84, 457, 397, 357, 124, 267, 230, 457, 219, 237, 298, 197, 137, 457, 367, 294, 276, 217, 442, 457, 108, 182, 332, 342, 366, 457, 322, 141, 279, 204, 253, 457, 112, 136, 236, 278, 209, 457, 112, 148, 220, 269, 220, 457, 224, 384, 303, 399, 264, 457, 205, 345, 315, 257, 112, 457, 219, 135, 231, 370, 359, 457, 215, 204, 310, 226, 23, 457, 378, 120, 217, 154, 43, 457, 376, 172, 189, 302, 419, 457, 352, 344, 285, 207, 423, 457, 219, 128, 316, 230, 286, 457, 295, 287, 185, 388, 432, 457, 170, 249, 268, 225, 327, 457, 315, 302, 276, 384, 440, 457]

decrypted = hash_words(["Voiture","Lover","Piscine","Chien"])
print(decrypted)