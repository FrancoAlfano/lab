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
    
    leido = os.read(fd, size)
    s_leido = bytes.decode(leido)

    header = check_header(s_leido)
    raster = check_raster(s_leido)

    if header != 0:
        header_byte = str.encode(header)
        os.write(fin, header_byte)
    else:
        print("error en header")

    if raster != 0:
        raster_byte = str.encode(raster)
        os.write(fin, raster_byte)
    else:
        print("error en raster")  
    

    os.close(fd)
    os.close(fin)

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
    header_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))'
    try:
        sucess = re.search(header_re, data)
        header = sucess.group(0)
        return header
    except AttributeError as err:
        print("Attribute ERROR: {0}".format(err))
        return 0

def check_raster(data):
    try:
        raster_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))(.*)'
        success = re.search(raster_re, data)
        raster = success.group(5)
        return raster
    except AttributeError as err:
        print("Attribute Error: {0}".format(err))
        return 0

if __name__ == "__main__":
    tp_1()