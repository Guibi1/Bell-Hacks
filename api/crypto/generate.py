from http.server import BaseHTTPRequestHandler
import random
import numpy as np
import json

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
              97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]
prime_list_larger_100 = [101, 103, 107, 109, 113, 127, 131, 137,
                         139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]


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


def generate_public_key(secretkey, publickeycount, modulus):
    vectorsize = len(secretkey)
    publickey = np.random.randint(100, 400, (publickeycount, vectorsize))
    publickeysecretkeymult = publickey * secretkey
    publickeysecretkeymultsum = publickeysecretkeymult.sum(axis=1)

    noise = np.random.randint(-4, 4, publickeycount)
    addednoise = np.add(noise, publickeysecretkeymultsum)
    addedmodulus = addednoise % modulus

    finalpublickey = np.column_stack((publickey, addedmodulus))
    finalpublickey = np.column_stack(
        (finalpublickey, np.ones([publickeycount, 1])*modulus))
    return finalpublickey


def publickeyarraytolist(input):
    flattened = [element for row in input for element in row]
    return flattened


def publicKeyApiGenerator(secretkey):
    secretkeyarr = hash_words(secretkey)
    publickey = generate_public_key(
        secretkeyarr, 20, random.choice(prime_list_larger_100))
    return np.array(publickeyarraytolist(publickey)).astype(int).tolist()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode('utf-8'))
        array = received_data.get("secretKey")
        key = publicKeyApiGenerator(array)
        keyjson = json.dumps(key)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(keyjson.encode('utf-8'))
