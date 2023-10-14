from http.server import BaseHTTPRequestHandler
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
    print(input)
    print(type(input))
    print(type(inputsecretkey))
    print(type(publickey))
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


def encryptedlisttoarray(input, publickey):
    width = publickey.shape[1]-1
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output


def publickeylisttoarray(input):
    width = 6
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output


def decryptPasswordApi(encryptedpassword, secretkeyinput, publickeyinput):
    publickey = publickeylisttoarray(publickeyinput)
    secretkey = hash_words(secretkeyinput)
    passwordarray = encryptedlisttoarray(encryptedpassword, publickey)

    print(publickey)
    print(secretkey)
    print(passwordarray)
    password = decryptstring(passwordarray, secretkey, publickey)
    return password


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode('utf-8'))
        encrypted_password = received_data.get("data")
        secret_key = received_data.get("secretKey")
        public_key = received_data.get("publicKey")
        decrypted_password = decryptPasswordApi(
            encrypted_password, secret_key, public_key)
        passwordjson = json.dumps({"result": decrypted_password})

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(passwordjson.encode('utf-8'))
