#Trabajo Practico n1

import argparse
import os
import re
import multiprocessing

def tp_1():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--red", help="Bytes de color rojo")
    parser.add_argument("-g", "--green", help="Bytes de color verde")
    parser.add_argument("-b", "--blue", help="Bytes de color azul")
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="nombre de la imagen", required=True)

    args = parser.parse_args()

    if args.red != None:
        red = int(args.red)
        print(red)
    
    if args.green != None:
        green = int(args.green)
        print(green)
    
    if args.blue != None:
        blue = int(args.blue)
        print(blue)

    size = int(args.size)
    archivo = args.file
    img = []
    
    fd = os.open(archivo, os.O_RDONLY)
    fin = os.open("prueba.ppm", os.O_RDWR|os.O_CREAT)

    while True:
        leido = os.read(fd, size)        
        img.append(leido)
        
        if len(leido) < size:
            print("\n\n\n END OF FILE!")
            break
    
    qData = multiprocessing.Queue()
    qFin = multiprocessing.Queue()
    qData.put(img)
    qFin.put(fin)

    proc = multiprocessing.Process(target=do_nothing,args=(qData,qFin,))
    proc.start()
    proc.join()

    listToStr = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])
  
    bytetost = str.encode(listToStr, encoding = "ISO-8859-1")

    #os.write(fin, bytetost)

    header = check_header(listToStr)
    raster = check_raster(listToStr)

    if header != 0:
        header_byte = str.encode(header)
        #os.write(fin, header_byte)
    else:
        print("error en header")

    if raster != 0:
        raster_byte = str.encode(raster)
        #os.write(fin, raster_byte)
    else:
        print("error en raster")

    '''
    for x in range(len(img)):
        os.write(fin, img[x])
    '''

    os.close(fd)
    os.close(fin)    

def do_nothing(qData, qFd):
    print("hola mi nombre es:", os.getpid(), " y mi padre es: ", os.getppid())
    fl = qFd.get()
    data = qData.get()
    for x in range(len(data)):
        os.write(fl, data[x])

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
        raster_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))(.*)'
        success = re.search(raster_re, data)
        raster = success.group(5)
        return raster
    except AttributeError as err:
        print("Attribute Error: {0}".format(err))
        return 0

if __name__ == "__main__":
    tp_1()