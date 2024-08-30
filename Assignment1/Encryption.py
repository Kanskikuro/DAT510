from caesarcipher import CaesarCipher

#Values
plainText = "Hoang-Ny William Nguyen Vo Security and Vulnerability in Networks"
CaeserKey =	24
NumericKey = 24513

#Substiutiopn part
substitutionCipherText = CaesarCipher(plainText, offset=24).encoded
print(substitutionCipherText)

#def transpositionCipher(key,textInput):