import math
import random
import string
import time
from caesarcipher import CaesarCipher

#Inital Values
plainText = "Hoang-Ny William Nguyen Vo Security and Vulnerability in Networks".lower().replace(" ", "")
CaeserKey =	24
NumericKey = 24513


#---------------Task1---------------------------------------------------------------------------------------------------------------------

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
        textList.append("x")
    
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
plainTextFlipped = "Boang-Ny William Nguyen Vo Security and Vulnerability in Networks".lower().replace(" ", "")
OptionBFlipped = transpositionCipher(NumericKey, CaesarCipher(plainTextFlipped, offset=24).encoded)

#How to convert string to binary
#https://stackoverflow.com/questions/18815820/how-to-convert-string-to-binary
def binaryConv(text):
    res = ''.join(format(ord(i), '08b') for i in text)
    return res
#How to count ones in binary and count ones in binary
#https://www.geeksforgeeks.org/count-set-bits-using-python-list-comprehension/
#https://stackoverflow.com/questions/19414093/how-to-xor-binary-with-python
def binaryDiff(a,b):
    a=binaryConv(a)
    b=binaryConv(b)
    
    Xor = int(a,2) ^ int(b,2)
    diffCount = '{0:b}'.format(Xor).count("1")
    return (diffCount/len(a))*100

#how to measure elapsed time
#https://www.programiz.com/python-programming/examples/elapsed-time
start = time.time()
for _ in range(16):
    plainTextFlipped = transpositionCipher(NumericKey, CaesarCipher(plainTextFlipped, offset=24).encoded).lower().replace(" ", "")
    print( plainTextFlipped + ' ' + str(time.time()-start) + ' ' + str(binaryDiff(plainTextFlipped,OptionB)))
