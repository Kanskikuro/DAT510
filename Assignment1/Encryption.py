import math
import random
import string
from caesarcipher import CaesarCipher

#Values
plainText = "Hoang-Ny William Nguyen Vo Security and Vulnerability in Networks"

CaeserKey =	24
NumericKey = 24513

#functions
def transpositionCipher(key,textInput):
    #Calculates variables for matrix size from the key
    keyLength = len(str(NumericKey))
    row = int(math.ceil(len(textInput)/keyLength))
    
    #Adding random letters to fill out the matrix
    textList= list(textInput)
    fill_null = int((row * keyLength) - len(textInput))
    for _ in range(fill_null):
        ranLetter = random.choice(string.ascii_lowercase)
        textList.append("X")
    
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
OptionB = transpositionCipher(NumericKey, CaesarCipher(plainText, offset=24).encoded).lower().replace(" ", "")

print(OptionB)