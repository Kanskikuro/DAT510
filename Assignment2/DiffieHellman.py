# ------------------------------------------Task l------------------------------------------
# Alice and Bob agreed to share public parameters p and g for the Diffie-Hellman protocol
# p is a large prime number and g is a generator, which is a primitive root mod p

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
