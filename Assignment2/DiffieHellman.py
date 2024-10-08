# ------------------------------------------Task l------------------------------------------
# Alice and Bob agreed to share public parameters p and g for the Diffie-Hellman protocol
# p is a large prime number and g is a generator, which is a primitive root mod p

import os
from Crypto.Cipher import AES
import numpy as np
import matplotlib.pyplot as plt
from caesarcipher import CaesarCipher
import time
import string
import random
import math
import hashlib
p = 353
g = 3
# Private keys
a = 97
b = 233

# p,g,a and b are numbers from the lecture.
# The public keys and secret key. A,B and S should be 40, 248 and 160 respectfully


def diffHellman(p, g, a, b):
    # Public keys
    A = pow(g, a, p)
    B = pow(g, b, p)
    # Secret key
    S = pow(A, b, p)
    return A, B, S

# The A, B and S are correct.
# This means the diffiehellman is implemented correctly, if the lecture example is correct.
# ------------------------------------------Task 2------------------------------------------


def hmac(key, msg):
    # HMAC(K, m) = hash ((K′ ⊕ opad) ∥ hash ((K′ ⊕ ipad) ∥ m))

    blockSize = 200  # 1600 bits

    # K'
    # checks if the secret key is long enough
    if len(key) > blockSize:
        key = hashlib.sha256(key)
    if len(key) < blockSize:
        key = key.ljust(blockSize, b'\0')  # pads the key with 0 bytes

    # ipad and opad
    ipad = bytes((x ^ 0x36) for x in key)
    opad = bytes((x ^ 0x5c) for x in key)

    # hash ((K′ ⊕ ipad) ∥ m)
    iHash = hashlib.sha256(ipad + msg).digest()

    # hash ((K′ ⊕ opad) ∥ iHash)
    oHash = hashlib.sha256(opad + iHash).digest()
    return oHash


def hmacVerify(key, msg, hmacMsg):
    return hmac(key, msg,) == hmacMsg


msg = b"hello world"
pubA, pubB, SecKey = diffHellman(p, g, a, b)
key_bytes = SecKey.to_bytes((SecKey.bit_length() + 7) // 8, byteorder='big')

print(hmacVerify(key_bytes, msg, hmac(key_bytes, msg)))


# -------------------Assignmen 1 Task 5


# Initial Values
plainText = "Hoang-Ny William Nguyen Vo Security and Vulnerability in Networks".lower().replace(" ", "")
CaesarKey = 24
NumericKey = 24513

def transpositionCipher(key, textInput):
    # Calculates variables for matrix size from the key
    keyLength = len(str(NumericKey))
    row = int(math.ceil(len(textInput)/keyLength))

    # Adding random letters to fill out the matrix
    textList = list(textInput)
    remainder = int((row * keyLength) - len(textInput))
    for _ in range(remainder):
        ranLetter = random.choice(string.ascii_lowercase)
        # appends a letter the remainder amount of times to fill out the matrix
        textList.append(ranLetter)

    # Create creating a matrix and inputting textInput
    matrix = [textList[i: i + keyLength]
              for i in range(0, len(textList), keyLength)]

    k = 0
    cipher = ""
    digitList = [int(digit) for digit in str(key)]
    # Reading the matrix with the numeric key order
    for _ in range(keyLength):
        # The digit value is the index of the order
        curr_idx = (digitList[k])-1
        cipher += ''.join([row[curr_idx]
                           for row in matrix])
        k += 1
    return cipher


def divideString(string, block_size):
    return [string[i:i + block_size] for i in range(0, len(string), block_size)]


def CTR(input):
    counter = 0
    nonce = os.urandom(int(len(input)/3))  # 3 blocks
    cipher = b""
    blocks = divideString(input, int(len(input)/3))
    for i in range(len(blocks)):
        # encrypts the block of plaintext
        blocks[i] = transpositionCipher(
            NumericKey, CaesarCipher(blocks[i], offset=24).encoded)
        counterNonce = nonce + counter.to_bytes(8, byteorder='big')
        counter = +1
        Xor = bytes(a ^ b for a, b in zip(
            counterNonce, blocks[i].encode('utf-8')))
        cipher += Xor
    return cipher


encryption = CTR(transpositionCipher(
    NumericKey, CaesarCipher(plainText, offset=24).encoded))
print(encryption)

#------------------------Task 3------------------------------------------