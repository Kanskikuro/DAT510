import math
import random
import string
import time
from caesarcipher import CaesarCipher
import matplotlib.pyplot as plt
import numpy as np
from Crypto.Cipher import AES
import os

#Initial Values
plainText = "Hoang-Ny William Nguyen Vo Security and Vulnerability in Networks".lower().replace(" ", "")
CaesarKey =	24
NumericKey = 24513

#---------------Task1---------------------------------------------------------------------------------------------------------------------

#Caesar cipher is imported as a library

#tutorial on how to make a transposition cipher
#https://www.geeksforgeeks.org/columnar-transposition-cipher/

def transpositionCipher(key,textInput):
    #Calculates variables for matrix size from the key
    keyLength = len(str(NumericKey))
    row = int(math.ceil(len(textInput)/keyLength))
    
    #Adding random letters to fill out the matrix
    textList= list(textInput)
    remainder = int((row * keyLength) - len(textInput))
    for _ in range(remainder):
        ranLetter = random.choice(string.ascii_lowercase)
        #appends a letter the remainder amount of times to fill out the matrix
        textList.append(ranLetter)
    
    #Create creating a matrix and inputting textInput
    matrix = [textList[i: i + keyLength]
            for i in range(0, len(textList), keyLength)]
    
    k=0
    cipher=""
    digitList = [int(digit) for digit in str(key)]
    #Reading the matrix with the numeric key order
    for _ in range(keyLength):
        #The digit value is the index of the order
        curr_idx = (digitList[k])-1
        cipher += ''.join([row[curr_idx]
                           for row in matrix])
        k += 1
    return cipher

#OptionA = CaesarCipher(transpositionCipher(NumericKey,plainText), offset=24).encoded.lower().replace(" ", "")
OptionB = transpositionCipher(NumericKey, CaesarCipher(plainText, offset=24).encoded)


#--------------Task2---------------------------------------------------------------------------------------------------------
#These are not used, because they were not correct. However the knowledge is used
#How to convert string to binary
#https://stackoverflow.com/questions/18815820/how-to-convert-string-to-binary
#How to count ones in binary and count ones in binary
#https://www.geeksforgeeks.org/count-set-bits-using-python-list-comprehension/
#https://stackoverflow.com/questions/19414093/how-to-xor-binary-with-python

plainTextFlipped = "Boang-Ny William Nguyen Vo Security and Vulnerability in Networks".lower().replace(" ", "")
OptionBFlipped = transpositionCipher(NumericKey, CaesarCipher(plainTextFlipped, offset=24).encoded)

#comparing letters
#https://stackoverflow.com/questions/35328953/how-to-compare-individual-characters-in-two-strings-in-python-3
def avalanche(a,b):
    l = 0
    for x, y in zip(a, b):
        if x == y:
            l=l+1
    return (l/len(a))*100

def avalancheBits(cipher1: bytes, cipher2: bytes) -> float:
    differing_bits = 0
    total_bits = len(cipher1) * 8

    for byte1, byte2 in zip(cipher1, cipher2):
        differing_bits += bin(byte1 ^ byte2).count('1')

    return (differing_bits / total_bits) * 100

#plotting
#https://www.w3schools.com/python/matplotlib_plotting.asp
x = np.array([])
y = np.array([])
#how to measure elapsed time
#https://www.programiz.com/python-programming/examples/elapsed-time
start = time.time()
for _ in range(20):
    plainTextFlipped = transpositionCipher(NumericKey, CaesarCipher(plainTextFlipped, offset=24).encoded)
    #print( str(avalanche(plainTextFlipped,OptionB))  + ' ' + str(time.time()-start))
    
    flipByte = plainTextFlipped.encode('utf-8')
    originalByte = OptionB.encode('utf8')
    print(avalancheBits(flipByte,originalByte))
    
    
    t = (time.time()-start)
   
    percent = avalanche(plainTextFlipped,OptionB)
    y = np.append(y,percent)
    x = np.append(x,t)

#the first element in the list is super inflated. It shows the 98, when avg is 3
x=x[1:]
y=y[1:]
    
plt.plot(y)
plt.xlabel("Iteration")
plt.ylabel("Differentiating bits in %")
#plt.show()
#-----------------Task5-----------------------------
#CTR
#uses the information on creating keys and counter/nonce, not tutorial
#https://onboardbase.com/blog/aes-encryption-decryption/

def divideString(string, block_size):
    return [string[i:i + block_size] for i in range(0, len(string), block_size)]

def CTR(input):
    counter = 0
    nonce = os.urandom(int(len(input)/3)) #3 blocks
    #plainTextByte = input.encode('utf-8')
    cipher = b""
    blocks = divideString(input,int(len(input)/3))
    for i in range(len(blocks)):
        #encrypts the block of plaintext
        blocks[i] = transpositionCipher(NumericKey, CaesarCipher(blocks[i], offset=24).encoded)
        counterNonce = nonce + counter.to_bytes(8, byteorder='big')
        counter=+1
        Xor = bytes(a ^ b for a, b in zip(counterNonce, blocks[i].encode('utf-8')))
        cipher += Xor
    return cipher

for _ in range(20):
    print(avalancheBits(CTR(plainText),OptionB.encode('utf-8')))
