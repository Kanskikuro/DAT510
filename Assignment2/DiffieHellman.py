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
    S = S.to_bytes((S.bit_length() + 7) // 8, byteorder='big')
    #print(A,B,S)
    return A, B, S

# The A, B and S are correct.
# This means the diffiehellman is implemented correctly, if the lecture example is correct.
# ------------------------------------------Task 2------------------------------------------


def hmac(key, msg):
    # HMAC(K, m) = hash ((K′ ⊕ opad) ∥ hash ((K′ ⊕ ipad) ∥ m))

    blockSize = 64  # 1600 bits

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

# print(hmacVerify(key_bytes, msg, hmac(key_bytes, msg)))

# ---------------------------------- Task 3 -------------------------------------------
# -------------------Assignmen 1 Task 5
# Initial Values
plainText = "Hoang-Ny William Nguyen Vo Security and Vulnerability in Networks".lower().replace(" ", "")
CaesarKey = 24
NumericKey = 24513


def transpositionCipher(key, textInput):
    # Calculates variables for matrix size from the key
    keyLength = len(str(key))
    row = int(math.ceil(len(textInput)/keyLength))

    # Adding random letters to fill out the matrix
    textList = list(textInput)
    remainder = int((row * keyLength) - len(textInput))
    for _ in range(remainder):
        ranLetter = random.choice(string.ascii_lowercase)
        # Appends a letter the remainder amount of times to fill out the matrix
        textList.append(ranLetter)

    # Create a matrix and inputting textInput
    matrix = [textList[i: i + keyLength]
              for i in range(0, len(textList), keyLength)]

    k = 0
    cipher = ""
    digitList = [int(digit) for digit in str(key)]
    # Reading the matrix with the numeric key order
    for _ in range(keyLength):
        # The digit value is the index of the order
        curr_idx = (digitList[k]) - 1
        cipher += ''.join([row[curr_idx] for row in matrix])
        k += 1
    return cipher


def divideString(string, block_size):
    return [string[i:i + block_size] for i in range(0, len(string), block_size)]


def CTR(input):
    counter = 0
    nonce = os.urandom(8)  # Generate a random nonce
    cipher = b""
    blocks = divideString(input, int(len(input)/3))

    for i in range(len(blocks)):
        # Encrypts the block of plaintext
        blocks[i] = transpositionCipher(
            NumericKey, CaesarCipher(blocks[i], CaesarKey).encode)

        counterNonce = nonce + counter.to_bytes(8, byteorder='big')
        counter += 1

        # XOR operation to encrypt
        Xor = bytes(a ^ b for a, b in zip(
            counterNonce, blocks[i].encode('utf-8')))
        cipher += Xor
    return nonce + cipher


def CTRDecrypt(input):
    nonce = input[:8]  # Extract nonce from the input
    input = input[8:]  # Remove nonce from the input
    counter = 0
    decryptedText = ""

    block_size = int(len(input) / 3)
    blocks = divideString(input, block_size)

    for i in range(len(blocks)):
        counterNonce = nonce + counter.to_bytes(8, byteorder='big')
        counter += 1

        # XOR to decrypt
        Xor = bytes(a ^ b for a, b in zip(
            counterNonce, blocks[i].decode('utf-8')))

        try:
            decryptedBlock = Xor.decode('utf-8')  # Decode the XOR result
            # Reverse the transposition applied earlier
            decryptedText += CaesarCipher(decryptedBlock,
                                          shift=-CaesarKey).decode()
        except UnicodeDecodeError:
            print(f"Error decoding block {i}: {Xor}")

    return decryptedText


# encryption = CTR(plainText)
# decryption = CTRDecrypt(encryption)
# print(decryption)
# ------------------------Task 4------------------------------------------


# step 1
pubA, pubB, SecKey = diffHellman(p, g, a, b)
msg = b"helloworld"
hmac(SecKey, msg)
# secKey is the initial chain key

# step 2 make a chainkeyHMAC
# prng for seed
p = 103
g = 5
# same private keys
_, _, seedKey = diffHellman(p, g, a, b)
random.seed(seedKey)

# Testing prng and observing byte conversion
for i in range(5):
    # 0-10 for simplicity, but can be any range. The bigger the more secure
    rand = random.randint(0, 10)
    randByt = rand.to_bytes((rand.bit_length() + 7) // 8, byteorder='big')
    # print(randByt, end="\t")


def chainHMAC(chainKey, type):
    # to create a new key each time,
    # adding the prng in bytes to the previous key
    # initial is diffie hellman
    if type == "ratchet":
        rand = random.randint(0, 10)
        randByt = rand.to_bytes((rand.bit_length() + 7) // 8, byteorder='big')
        # adding chainkey to the randbyte to create a new messagekey
        # print(chainKey, randByt , chainKey+randByt)
        return chainKey+randByt
    else:
        return hmac(chainKey, type)

chainKey = SecKey
for i in range(5):
    chainKey = chainHMAC(chainKey, "ratchet")
    res = chainHMAC(chainKey, b"hello world")
    print(res)

# --------------------------------Task 5------------------------------------
# first, make functions that create new prime and base for Diffie-hellman key exchange
# https://stackoverflow.com/questions/27831283/random-prime-number-in-python


def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True
# https://stackoverflow.com/questions/40190849/efficient-finding-primitive-roots-modulo-n-using-python


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def primRoots(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}][0]


# Generates new prime
primes = [i for i in range(0, 100) if isPrime(i)]

# n = random.choice(primes)
# m = primRoots(n)
# print(n)
# print(m)


def doubleRatchet(K, input):
    # new RootKey
    if input == SecKey:
        n = random.choice(primes)
        m = primRoots(n)
        _, _, rootKey = diffHellman(n, m, a, b)
        # print(n,m,rootKey)
        return rootKey
    else:
        # new chainkey and msgTag
        chainKey = chainHMAC(K, "ratchet")
        msgTag = chainHMAC(chainKey, input)
        return chainKey, msgTag


for i in range(20):
    # new rootkey every 5th msg
    if i % 5 == 0:
        RootKey = doubleRatchet(_, SecKey)
        chainKey = RootKey
        # print("New RootKey")

    chainKey, msgTag = doubleRatchet(chainKey, b"hello world")
    # print(chainKey, msgTag)
