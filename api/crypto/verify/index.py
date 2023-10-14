from http.server import BaseHTTPRequestHandler
import random
import numpy as np
import json

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
              97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]


def find_closest_prime(target, prime_list):
    closest_prime = None
    min_difference = float('inf')

    for prime in prime_list:
        difference = abs(target - prime)
        if difference < min_difference:
            min_difference = difference
            closest_prime = prime

    return closest_prime


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
        current_char += 1
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


def decryptdata(input, inputsecretkey, publickey):
    decryptarray = []
    inputmodulus = publickey[0, publickey.shape[1]-1]

    u = input[:, :input.shape[1]-1]
    v = input[:, input.shape[1]-1]
    i = 0
    halfmod = int(inputmodulus/2)
    while (i < len(input)):

        dec = (v[i] - np.matmul(inputsecretkey, u[i])).__mod__(inputmodulus)
        if (((inputmodulus - dec) < abs(halfmod-dec)) or ((dec) < abs(halfmod-dec))):
            val = 0
        else:
            val = 1
        decryptarray.append(val)
        i += 1

    return decryptarray


def encryptbyte(input, inputpublickey):
    encryptedarray = []
    inputmodulus = int(inputpublickey[0, inputpublickey.shape[1]-1])
    binary_representation = input
    bits = np.array([int(bit) for bit in binary_representation], dtype=int)
    pk = inputpublickey[:, :inputpublickey.shape[1]-2]
    pkr = inputpublickey[:, inputpublickey.shape[1] -
                         2:inputpublickey.shape[1]-1]
    i = 0
    while (i < bits.shape[0]):

        currentbit = bits[i]
        randpublickeys = np.random.randint(0, inputpublickey.shape[0]-1, 5)
        u = (pk[randpublickeys[0]] + pk[randpublickeys[1]] + pk[randpublickeys[2]
                                                                ]+pk[randpublickeys[3]]+pk[randpublickeys[4]]).__mod__(inputmodulus)
        v = ((pkr[randpublickeys[0]] + pkr[randpublickeys[1]] + pkr[randpublickeys[2]]+pkr[randpublickeys[3]
                                                                                           ]+pkr[randpublickeys[4]]) + int(inputmodulus/2)*currentbit).__mod__(inputmodulus)

        appended = np.append(u, v)
        encryptedarray.append(appended)
        i += 1

    encryptedarray = np.array(encryptedarray)
    return encryptedarray


def encryptcharacter(input, inputpublickey):
    char_num = ord(input)
    char_bin = np.binary_repr(char_num, 8)
    encrypted_byte = encryptbyte(char_bin, inputpublickey)
    return encrypted_byte


def encryptstring(input, inputpublickey):
    input = str(input)
    encryptedarray = np.empty(shape=[0, 5])
    for chars in input:
        encryptedchar = encryptcharacter(chars, inputpublickey)
        encryptedarray = np.vstack((encryptedarray, encryptedchar))

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
        output += currentchar
        i += 1

    return output


def publickeylisttoarray(input):
    width = 6
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output


def verifySecretKey(secretkey, publickey):
    if (len(secretkey) == 4):
        publickeyarr = publickeylisttoarray(publickey)
        secretkeyarr = hash_words(secretkey)
        testmessage = str(random.randint(256, 512))
        if (testmessage == decryptstring((encryptstring(testmessage, publickeyarr)), secretkeyarr, publickeyarr)):
            return True
        else:
            return False
    else:
        return False


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode('utf-8'))
        secret_key = received_data.get("secretKey")
        public_key = received_data.get("publicKey")
        verification_boolean = verifySecretKey(secret_key, public_key)
        answer = json.dumps({'success': verification_boolean})

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(answer.encode('utf-8'))
