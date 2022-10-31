#Hidding files in Images Yassine SABIR

import cv2
import numpy as np

def int2bin(n):
    if n==0:
        return "0"
    return int2bin(n//2)+str(n%2)

def str_len_8(s):
    L="00000000"+s
    return L[-8:]


def bin2int(b):
    if b=="":
        return 0
    return int(b[-1])+2*bin2int(b[:-1])

def cryptRGB(Value,b):
    if b=='1' and Value%2==0:
        return Value + 1
    elif b=='1' and Value%2==1:
        return Value
    elif b=='0' and Value%2==0:
        return Value
    else:
        return Value-1

def hiding(img_path,file_path):

    img = cv2.imread(img_path)

    file = open(file_path,"rb")

    content = file.read()

    len_file = len(content)

    n,m,d = img.shape

    if d!=3:
        print("ERROR")
        return

    newimg=np.zeros((n,m,d),np.uint8)

    index=0

    binary = ""

    i,j = 0,0

    counter = 0

    while(1):

        if counter == 8:
            counter = 0

        if counter == 0:

            if index+2 < len_file:
                binary = str_len_8(int2bin(content[index]))+str_len_8(int2bin(content[index+1]))+str_len_8(int2bin(content[index+2]))

            elif index+1 < len_file:
                binary = str_len_8(int2bin(content[index]))+str_len_8(int2bin(content[index+1]))+str_len_8(int2bin(0))

            elif index < len_file:
                binary = str_len_8(int2bin(content[index]))+str_len_8(int2bin(0))+str_len_8(int2bin(0))

            else:
                binary = str_len_8(int2bin(0))+str_len_8(int2bin(0))+str_len_8(int2bin(0))

            index+=3

        if j >= m:
            i+=1
            j=0

        if i < n:
            newimg[i][j] = (cryptRGB(img[i][j][0],binary[3*counter]),cryptRGB(img[i][j][1],binary[3*counter+1]),cryptRGB(img[i][j][2],binary[3*counter+2]))
            counter += 1
            j += 1

        else:
            file.close()
            return newimg


def showing(img,file_path):

    file=open(file_path,"wb")

    n,m,_ = img.shape

    binary = ""

    for i in range(n):
        for j in range(m):

            binary += str(img[i][j][0]%2)

            if len(binary) == 8:
                file.write(int(binary,2).to_bytes(1,"little"))
                binary = ""

            binary += str(img[i][j][1]%2)

            if len(binary) == 8:
                file.write(int(binary,2).to_bytes(1,"little"))
                binary = ""

            binary += str(img[i][j][2]%2)

            if len(binary) == 8:
                file.write(int(binary,2).to_bytes(1,"little"))
                binary = ""


    if binary != "":
        file.write(int((binary+"00000000")[:8],2).to_bytes(1,"little"))

    file.close()


