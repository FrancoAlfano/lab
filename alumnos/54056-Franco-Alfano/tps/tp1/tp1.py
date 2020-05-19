#Trabajo Practico n1

import argparse
import os
import re
import multiprocessing
import array
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def tp_1():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--red", help="Bytes de color rojo")
    parser.add_argument("-g", "--green", help="Bytes de color verde")
    parser.add_argument("-b", "--blue", help="Bytes de color azul")
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="nombre de la imagen", required=True)

    args = parser.parse_args()
    
    #Para el histograma
    numeros = []

    if args.red != None:
        rojo = float(args.red)
        numeros.append(rojo)
    
    if args.green != None:
        verde = int(args.green)
        numeros.append(verde)
    
    if args.blue != None:
        azul = int(args.blue)
        numeros.append(azul)

    size = int(args.size)
    archivo = args.file
    img = []
    
    try:
        fd = os.open(archivo, os.O_RDONLY)    
        while True:
            leido = os.read(fd, size)        
            img.append(leido)            
            if len(leido) < size:
                print("\n\n\nEND OF FILE!")
                break
        
        q_red = multiprocessing.Queue()
        q_green = multiprocessing.Queue()
        q_blue = multiprocessing.Queue()

        listToStr = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])

        q_red.put(listToStr)
        q_green.put(listToStr)
        q_blue.put(listToStr)
    
        header = check_header(listToStr)        
        if header != 0:
            header_byte = str.encode(header, encoding = "ISO-8859-1")
        else:
            print("error en header")

        h_red = multiprocessing.Process(target=red_img,args=(q_red, header_byte,rojo,))
        h_green = multiprocessing.Process(target=green_img,args=(q_green, header_byte,verde,))
        h_blue = multiprocessing.Process(target=blue_img,args=(q_blue, header_byte,azul,))

        h_red.start()
        h_green.start()
        h_blue.start()

        h_red.join()
        h_green.join()
        h_blue.join()

        os.close(fd)

        histograma(numeros)
        print("Procesos Exitoso!")

    except FileNotFoundError as err:
        print(err)


def red_img(q_red, header_byte, rojo):
    print("hola mi nombre es:", os.getpid(), " y mi padre es: ", os.getppid())

    i_red = os.open("red.ppm", os.O_RDWR|os.O_CREAT)
    data = q_red.get()
    raster = check_raster(data)
    if raster != 0:
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")

    red = []

    for i in range(0,len(raster_byte),3):
        bit = raster_byte[i]*rojo
        if bit > 255:
            bit = 255
        red.append(bit)
        red.append(0)
        red.append(0)  

    red = array.array('B',red)
    os.write(i_red, header_byte)
    os.write(i_red, red)
    os.close(i_red)

    print("done")
    


def green_img(q_green, header_byte, verde):
    print("hola mi nombre es:", os.getpid(), " y mi padre es: ", os.getppid())
    i_green = os.open("green.ppm", os.O_RDWR|os.O_CREAT)
    data = q_green.get()
    raster = check_raster(data)
    if raster != 0:
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")

    green = []

    for i in range(1,len(raster_byte),3):
        bit = raster_byte[i]*verde
        if bit > 255:
            bit = 255
        green.append(0)
        green.append(bit)
        green.append(0)   

    green = array.array('B',green)
    os.write(i_green, header_byte)
    os.write(i_green, green)
    os.close(i_green)

    print("done")

def blue_img(q_blue, header_byte, azul):
    print("hola mi nombre es:", os.getpid(), " y mi padre es: ", os.getppid())
    i_blue = os.open("blue.ppm", os.O_RDWR|os.O_CREAT)
    data = q_blue.get()
    raster = check_raster(data)
    if raster != 0:
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")

    blue = []

    for i in range(2,len(raster_byte),3):
        bit = raster_byte[i]*azul
        if bit > 255:
            bit = 255
        blue.append(0)
        blue.append(0)   
        blue.append(bit)

    blue = array.array('B',blue)
    os.write(i_blue, header_byte)
    os.write(i_blue, blue)
    os.close(i_blue)

    print("done")

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
        raster_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))([\s\S]*)'
        success = re.search(raster_re, data)
        raster = success.group(5)
        return raster
    except AttributeError as err:
        print("Attribute Error: {0}".format(err))
        return 0

def histograma(numeros):
    word_list = []

    red = ["red"] * numeros[0]
    green = ["green"] * numeros[1]
    blue = ["blue"] * numeros[2]

    word_list = red + green + blue
    counts = Counter(word_list)
    labels, values = zip(*counts.items())

    # sort your values in descending order
    indSort = np.argsort(values)[::-1]

    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]

    indexes = np.arange(len(labels))
    plt.bar(indexes, values)

    # add labels
    plt.xticks(indexes, labels)
    plt.show()


if __name__ == "__main__":
    tp_1()