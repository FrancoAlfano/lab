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
            print("\n\n\nEND OF FILE!")
            break
    
    q_header = multiprocessing.Queue()
    q_raster = multiprocessing.Queue()
    q_fin = multiprocessing.Queue()
    q_fin.put(fin)    

    listToStr = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])
  

    header = check_header(listToStr)
    raster = check_raster(listToStr)

    #bytetost = str.encode(listToStr, encoding = "ISO-8859-1")
    
    if header != 0:
        header_byte = str.encode(header, encoding = "ISO-8859-1")
        q_header.put(header_byte)
    else:
        print("error en header")

    if raster != 0:
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")
        q_raster.put(raster_byte)
    else:
        print("error en raster")
    
    proc = multiprocessing.Process(target=make_file,args=(q_header, q_raster,q_fin,))    
    proc.start()
    proc.join()

    '''
    for x in range(len(img)):
        os.write(fin, img[x])
    '''

    os.close(fd)
    os.close(fin)

def make_file(q_header, q_raster, q_fin):
    print("hola mi nombre es:", os.getpid(), " y mi padre es: ", os.getppid())
    fin = q_fin.get()
    header = q_header.get()
    raster = q_raster.get()

    br = int.from_bytes(raster, byteorder='big')

    print(str(br)[0:50])
    
    br = br*2

    br2 = br.to_bytes((br.bit_length() + 7) // 8, 'big')


    os.write(fin, header)
    os.write(fin, br2)

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

if __name__ == "__main__":
    tp_1()