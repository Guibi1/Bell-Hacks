from http.server import BaseHTTPRequestHandler
import numpy as np
import json


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


def encryptedarraytolist(input):
    flattened = [element for row in input for element in row]
    return flattened


def publickeylisttoarray(input):
    width = 6
    output = np.array([input[i:i+width] for i in range(0, len(input), width)])
    return output


def encryptPasswordApi(password, publickeyinput):
    publickey = publickeylisttoarray(publickeyinput)
    encryptedpassword = encryptstring(password, publickey)
    return (np.array(encryptedarraytolist(encryptedpassword)).astype(int)).tolist()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode('utf-8'))
        decrypted_password = received_data.get("data")
        public_key = received_data.get("publicKey")
        encrypted_password = encryptPasswordApi(decrypted_password, public_key)
        passwordjson = json.dumps(encrypted_password)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(passwordjson.encode('utf-8'))
