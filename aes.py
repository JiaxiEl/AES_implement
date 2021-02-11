"""
Author: JiaxiChen
Programming information: Encryption and decryption   no padding becasue fit 128 bits
"""



"""
plaintext:abcdefghijklmnop
a e i m
b f j n
c g k o
d h l p
from top to bottom and left to right

"""
#Forward S-box for AES_SubBytes
s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)
#Inverse S-box for AES_Inverse SubBytes
inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)
rCon = (
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
)

#Change text to Matrix
def textToMatrix(text):
    matrix = []
    for i, fillMartix in zip(range(16), text):
        if i < 4:
            matrix.append([ord(fillMartix)])
        else:
            matrix[int(i % 4)].append(ord(fillMartix))
    return matrix


#Change text to matrix
def matrixToText(matrix):
    text =''
    for i in range(4):
        for j in range(4):
            text += chr(matrix[j][i])
    return text

"""
Multiplication rule: multiplication of a value by 02 can be implemented as
a 1-bit left shift followed by a conditional bitwise XOR with (00011011) if the
leftmost bit of the original value (before the shift) is 1
"""
#Way for mix_column
mul02 = lambda num: (((num << 1) ^ 0x1B) & 0xFF) if (num & 0x80) else (num << 1)
mul03 = lambda num: mul02(num)^num
mul09 = lambda num: mul02(mul02(mul02(num)))^num
mul0b = lambda num: mul02(mul02(mul02(num)))^mul02(num)^num
mul0d = lambda num: mul02(mul02(mul02(num)))^mul02(mul02(num))^num
mul0e = lambda num: mul02(mul02(mul02(num)))^mul02(mul02(num))^mul02(num)



def key_Expansion(key):
    roundKey = textToMatrix(key)
    for i in range(1, 11):
        for j in range(4):
            roundKey.append([])
            if j == 0:
                keysolt = s_box[roundKey[i * 4 - 4 + (j +1) % 4][3]] ^ roundKey[i * 4 - 4 + j][0] ^rCon[i-1]
            else:
                keysolt = s_box[roundKey[i * 4 - 4 + (j +1) % 4][3]] ^ roundKey[i * 4 - 4 + j][0]
            roundKey[i*4+j].append(keysolt)
        for k in range(4):
            for s in range(1, 4):

                keysolt = roundKey[(i-1)*4+k][s]^roundKey[i*4+k][s-1]
                roundKey[i * 4 + k].append(keysolt)
    return roundKey





#AES-subBytes: lookup the s_box table
def subBytes(textMatrix):
    for i in range(4):
        for j in range(4):
            textMatrix[i][j] = s_box[textMatrix[i][j]]


#AES-subBytes: lookup the inv_s_box table
def inv_subBytes(textMatrix):
    for i in range(4):
        for j in range(4):
            textMatrix[i][j] = inv_s_box[textMatrix[i][j]]



"""
AES shiftRows
First row: no change
Second row: shift 1
Third row: shift 2
Forth row: shift 3
textM: textMatrix
"""
#Doing shift row
def shiftRows(textM):
    textM[1][0], textM[1][1], textM[1][2], textM[1][3] = textM[1][1], textM[1][2], textM[1][3], textM[1][0]
    textM[2][0], textM[2][1], textM[2][2], textM[2][3] = textM[2][2], textM[2][3], textM[2][0], textM[2][1]
    textM[3][0], textM[3][1], textM[3][2], textM[3][3] = textM[3][3], textM[3][0], textM[3][1], textM[3][2]


#inverse way to do shift row
def inv_shiftRows(textM):
    textM[1][0], textM[1][1], textM[1][2], textM[1][3] = textM[1][3], textM[1][0], textM[1][1], textM[1][2]
    textM[2][0], textM[2][1], textM[2][2], textM[2][3] = textM[2][2], textM[2][3], textM[2][0], textM[2][1]
    textM[3][0], textM[3][1], textM[3][2], textM[3][3] = textM[3][1], textM[3][2], textM[3][3], textM[3][0]



def add_round_key(textMatrix,key):
    for i in range(4):
        for j in range(4):
            textMatrix[i][j] ^= key[i][j]

"""
02  03  01  01
01  02  03  01
01  01  02  03
03  01  01  02
"""
#mix column
def mix_Col(textM):
    for i in range(4):
        s1 = mul02(textM[0][i])^mul03(textM[1][i])^(textM[2][i])^(textM[3][i])
        s2 = (textM[0][i])^mul02(textM[1][i])^mul03(textM[2][i])^(textM[3][i])
        s3 = (textM[0][i])^(textM[1][i])^mul02(textM[2][i])^mul03(textM[3][i])
        s4 = mul03(textM[0][i])^(textM[1][i])^(textM[2][i])^mul02(textM[3][i])
        textM[0][i] = s1
        textM[1][i] = s2
        textM[2][i] = s3
        textM[3][i] = s4

"""
0E  0B  0D  09     
09  0E  0B  0D     
0D  09  0E  0B     
0B  0D  09  0E     
"""

#inverse way to do mix column
def inv_mix_Col(textM):
    for i in range(4):
        s1 = mul0e(textM[0][i])^mul0b(textM[1][i])^mul0d(textM[2][i])^mul09(textM[3][i])
        s2 = mul09(textM[0][i])^mul0e(textM[1][i])^mul0b(textM[2][i])^mul0d(textM[3][i])
        s3 = mul0d(textM[0][i])^mul09(textM[1][i])^mul0e(textM[2][i])^mul0b(textM[3][i])
        s4 = mul0b(textM[0][i])^mul0d(textM[1][i])^mul09(textM[2][i])^mul0e(textM[3][i])
        textM[0][i] = s1
        textM[1][i] = s2
        textM[2][i] = s3
        textM[3][i] = s4


#round encrypt
def doEncryption(text,key):
    subBytes(text)
    shiftRows(text)
    mix_Col(text)
    add_round_key(text,key)

#round decrypt
def doDecryption(text,key):
    add_round_key(text, key)
    inv_mix_Col(text)
    inv_shiftRows(text)
    inv_subBytes(text)



def encryptFile(file_reference, key):
    keyMartix = key_Expansion(key)
    inputText =file_reference.read()
    file_reference.seek(0)
    file_reference.truncate()
    count = 0
    while True:
        plaintext = inputText[count:count+16]
        if count >= len(inputText):
            break
        textMatrix = textToMatrix(plaintext)
        add_round_key(textMatrix, keyMartix[:4])
        for i in range(1, 10):
            doEncryption(textMatrix,keyMartix[4*i:4*(i+1)])
        subBytes(textMatrix)
        shiftRows(textMatrix)
        add_round_key(textMatrix,keyMartix[40:])
        file_reference.write(matrixToText(textMatrix))
        count += 16




def decryptFile(file_reference, key):
    keyMartix = key_Expansion(key)
    file_reference.seek(0)
    inputText = file_reference.read()
    file_reference.seek(0)
    file_reference.truncate()

    count = 0
    while True:
        cipertext = inputText[count:count + 16]
        if count >= len(inputText):
            break
        textMatrix = textToMatrix(cipertext)
        add_round_key(textMatrix,keyMartix[40:])
        inv_shiftRows(textMatrix)
        inv_subBytes(textMatrix)
        for i in range(9,0,-1):
            doDecryption(textMatrix,keyMartix[4*i:4*(i+1)])
        add_round_key(textMatrix,keyMartix[:4])
        file_reference.write(matrixToText(textMatrix))
        count += 16


if __name__ == '__main__':
    File_reference = open("demofile.txt", "r+")
    encryptFile(File_reference,"thisisakeyforaes")
    decryptFile(File_reference,"thisisakeyforaes")




