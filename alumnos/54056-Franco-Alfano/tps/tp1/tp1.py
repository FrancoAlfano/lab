#Trabajo Practico n1

import argparse
import os
import re

def tp_1():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--red", help="Bytes de color rojo")
    parser.add_argument("-g", "--green", help="Bytes de color verde")
    parser.add_argument("-b", "--blue", help="Bytes de color azul")
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="nombre de la imagen", required=True)

    args = parser.parse_args()
    red = int(args.red)
    green = int(args.green)
    blue = int(args.blue)
    size = int(args.size)
    archivo = args.file   
    
    fd = os.open(archivo, os.O_RDONLY)
    fin = os.open("prueba.ppm", os.O_RDWR|os.O_CREAT)
    num = os.open("num.ppm", os.O_RDWR|os.O_CREAT)
    best = os.open("best.ppm", os.O_RDWR|os.O_CREAT)
    
    leido = os.read(fd, 100)
    print("\nLEIDO TYPE ", type(leido))
    os.write(best, leido)
    print("\n\nLEIDOOOO: ", leido)
    lei2 = str(leido)
    print("\n\nLEIDO AS STRING: ", lei2)
    b1 = bytes(lei2, encoding = 'utf-8')
    print("\n\nBYYYYYYYYTES: ",b1)
    os.write(num, b1)

    header = check_header(leido)
    raster = check_raster(leido)

    header_byte = str.encode(header)
    raster_byte = str.encode(raster)

    os.write(fin, header_byte)
    os.write(fin, raster_byte)

    os.close(fd)
    os.close(fin)
    os.close(num)
    os.close(best)

    '''
    while True:
        leido = os.read(fd, size)        
        header = check_header(leido)      
        break
    '''
    '''
    if len(leido) < int(args.size):
        print("\n\n\n END OF FILE!")
        break
    '''

def check_header(data):
    header_re = r'(P6\\n)((#\s*\w*\s*\w*\\n\d* \d*\\n\d*\\n)|(\d* \d*\\n\d*\\n))'
    sucess = re.search(header_re, str(data))
    header = sucess.group(0)
    print("\n\nHEADERRRRrrrrrRRRR: ", header)
    return header

def check_raster(data):
    raster_re = r'(P6\\n)((#\s*\w*\s*\w*\\n\d* \d*\\n\d*\\n)|(\d* \d*\\n\d*\\n))(.*)'
    success = re.search(raster_re, str(data))
    return success.group(5)

if __name__ == "__main__":
    tp_1()