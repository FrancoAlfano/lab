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
    fin = os.open("test.ppm", os.O_WRONLY|os.O_CREAT)

    while True:
        leido = os.read(fd, size)        
        header = check_header(leido)      
        image = check_raster(leido)
        break

    os.write(fin, str.encode(header))

    '''
    if len(leido) < int(args.size):
        print("\n\n\n END OF FILE!")
        break
    '''

def check_header(data):
    header_re = r'P6\\n\d*\s\d*\\n\d*'
    sucess = re.search(header_re, str(data))
    print(sucess.group(0))
    return sucess.group(0)

def check_raster(data):
    raster_re = r'P6\\n\d*\s\d*\\n\d*'
    sucess = re.search(header_re, str(data))
    print(sucess.group(0))
    return sucess.group(0)


if __name__ == "__main__":
    tp_1()