# ------------------------------------------Task l------------------------------------------
# Alice and Bob agreed to share public parameters p and g for the Diffie-Hellman protocol
# p is a large prime number and g is a generator, which is a primitive root mod p

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
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
    # print(A,B,S)
    return A, B, S

# The A, B and S are correct.
# This means the diffiehellman is implemented correctly, if the lecture example is correct.
# ------------------------------------------Task 2------------------------------------------
# This HMAC with XOR as hash


def xor(a, b):
    # Checks for length and takes the smallest one
    length = min(len(a), len(b))
    return bytes([b1 ^ b2 for b1, b2 in zip(a[:length], b[:length])])


def hmacXor(key, msg):
    # HMAC(K, m) = hash ((K′ ⊕ opad) ∥ hash ((K′ ⊕ ipad) ∥ m))
    blockSize = 64  # 1600 bits

    # K'
    # Check if the secret key is too long or too short
    if len(key) > blockSize:
        # Xor will not make the key shorter,
        # so the key is truncated to the blockSize
        key = key[:blockSize]
    if len(key) < blockSize:
        # Pad the key with 0 bytes to match blockSize
        key = key.ljust(blockSize, b'\0')

    # ipad and opad
    ipad = bytes((x ^ 0x36) for x in key)
    opad = bytes((x ^ 0x5c) for x in key)

    # XOR ((K′ ⊕ ipad) ∥ m)
    ixor = xor(ipad, msg)

    # XOR ((K′ ⊕ opad) ∥ inner_xor)
    oxor = xor(opad, ixor)

    return oxor


# This HMAC improves on the HMAC given by the task by using SHA instead of Xor
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


def hmacVerify(key, msg, tag):
    return hmac(key, msg,) == tag


msg = b"hello world"
pubA, pubB, SecKey = diffHellman(p, g, a, b)

# Testing HMAC
# print(hmacVerify(SecKey, msg, hmac(SecKey, msg)))
# print(hmacVerify(SecKey, msg, hmac(SecKey, b"hello worll")))

# print(hmacXor(SecKey, msg) == hmacXor(SecKey, msg))
# print(hmacXor(SecKey, msg) == hmacXor(SecKey, b"hello worll"))

# ---------------------------------- Task 3 -------------------------------------------
# encryption from task 3 was not implemented correctly, so AES is used instead
# https://onboardbase.com/blog/aes-encryption-decryption/


def aesEncryption(SecKey, msg):
    # A new key. Reusing the same key is not secure
    aesKey = get_random_bytes(16)

    cipher = AES.new(aesKey, AES.MODE_EAX)
    hmac(SecKey, msg)
    ciphertext = cipher.encrypt(msg+hmac(SecKey, msg))
    nonce = cipher.nonce
    return ciphertext, nonce, aesKey


def aesDecrypt(ciphertext, aesKey, nonce):
    cipher = AES.new(aesKey, AES.MODE_EAX, nonce)
    data = cipher.decrypt(ciphertext)
    # Knows the size of HMAC, 64 bytes
    msgDecrypted = data[:-32]
    tag = data[len(msg):]
    return msgDecrypted, tag


msg = b'hello world'
ciphertext, nonce, aesKey = aesEncryption(SecKey, msg)
msgDecrypt, tag = aesDecrypt(ciphertext, aesKey, nonce)

# print(hmacVerify(SecKey, msg, tag))

# ------------------------Task 4------------------------------------------
# step 1, Diff-Hellman key exchange
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


def chainHMAC(chainKey, input):
    # to create a new key each time,
    # adding the prng in bytes to the previous key
    # initial is diffie hellman
    if input == "ratchet":
        rand = random.randint(0, 10)
        randByt = rand.to_bytes((rand.bit_length() + 7) // 8, byteorder='big')
        # adding chainkey to the randbyte to create a new messagekey
        # print(chainKey, randByt , chainKey+randByt)
        return chainKey+randByt
    else:
        return aesEncryption(chainKey, input)


chainKey = SecKey
for i in range(5):
    chainKey = chainHMAC(chainKey, "ratchet")
    ciphertext, nonce, aesKey = chainHMAC(chainKey, b"hello")
    msgDecrypt, tag = aesDecrypt(ciphertext, aesKey, nonce)
    # print(msgDecrypt)
    # print(tag)


# Improving on the task
# The seed will be made the same way since it was a good solution to create a secure shared seed key
random.seed(seedKey)

# the improved task will mostly be the same.
# mostly integrating the singleratchet so its one function, instead of two.


def singleRat(chainKey, input):
    # from testing, the random int should be bigger to avoid collision
    # the key should match the size
    # this does not completely avoid collision. Its better to use better PRNG algorisms
    # random.randint() is the most simple PRNG
    rand = random.randint(0, 1000)
    randByt = rand.to_bytes((rand.bit_length() + 7) // 8, byteorder='big')
    # simple xor encryption of the key
    chainKey = xor(chainKey, randByt)

    return aesEncryption(chainKey, input)


chainKey = SecKey
byteList = [b'this', b'is', b'a', b'test', b'!']
for i in range(5):
    chipertext, nonce, aesKey = singleRat(chainKey, byteList[i])
    msgDecrypt, tag = aesDecrypt(chipertext, aesKey, nonce)
    # print(msgDecrypt)
    print(tag)

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


# Generates new prime, then randomly picks
primes = [i for i in range(0, 1000) if isPrime(i)]

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

# Improving task
# same improvements from task 4, removing unnecessary labels and make it to one function instead of 3 different steps
# Keeping it simple by letting in a iteration input
# still using isprime, gcd and primeroots as a solution to make new public keys -> new shared keys


def doubleRat(chainKey, input, iteration):
    if iteration % 5 == 0:
        n = random.choice(primes)
        m = primRoots(n)
        _, _, rootKey = diffHellman(n, m, a, b)
        chainKey = rootKey
        print("new Root key")

    return singleRat(chainKey, input)

chainKey = SecKey
byteList = [b'this', b'is', b'a', b'test', b'!']
for i in range(20):
    ciphertext, nonce, aesKey = doubleRat(chainKey, byteList[i%5], i)
    msg, tag = aesDecrypt(ciphertext, aesKey, nonce)
    #print(msg)
    #print(ciphertext)
    print(tag)