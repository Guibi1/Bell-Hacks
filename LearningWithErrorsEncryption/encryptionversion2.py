import numpy as np
import math



def generate_key_pair(secretkey, publickeycount, modulus):
    vectorsize = len(secretkey)

    publickey = np.random.randint(100, 400, (publickeycount, vectorsize))

    publickeysecretkeymult = publickey * secretkey

    publickeysecretkeymultsum = publickeysecretkeymult.sum(axis=1)

    noise = np.random.randint(-4, 4, publickeycount)

    addednoise = np.add(noise, publickeysecretkeymultsum)

    addedmodulus = addednoise % modulus

    finalpublickey = np.column_stack((publickey, addedmodulus))
    
    finalpublickey = np.column_stack((finalpublickey,np.ones([publickeycount,1])*modulus))
    
    return secretkey, finalpublickey



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

def decryptdata(input, inputsecretkeywmod):
    decryptarray = []
    inputmodulus = inputsecretkeywmod[inputsecretkeywmod.shape[0]-1]
    inputsecretkey = inputsecretkeywmod[:inputsecretkeywmod.shape[0]-1]
    u = input[:,:input.shape[1]-1]
    v = input[:,input.shape[1]-1]
    i = 0
    halfmod = int(inputmodulus/2)
    while (i < len(input)):
        
        dec = (v[i] - np.matmul(inputsecretkey,u[i])).__mod__(inputmodulus)
        if (((modulus - dec) < abs(halfmod-dec)) or ((dec) < abs(halfmod-dec))): 
            val = 0
        else:
            val = 1
        decryptarray.append(val)
        i+=1    

    return decryptarray

vectorsize = 20
publickeycount = 300
modulus = 101
secretkey, publickey = generate_key_pair(vectorsize, publickeycount, modulus)

encrypted = encryptdata(210,publickey)
print(encrypted)
decryptdata = decryptdata(encrypted,secretkey)
print(decryptdata)
