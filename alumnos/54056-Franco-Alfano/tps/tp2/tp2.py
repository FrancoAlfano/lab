#Trabajo Practico n°2

import argparse
import os
import re
import threading
import binascii

text = []
barrera = threading.Barrier(3)

def tp_2():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="Archivo portador", required=True)
    parser.add_argument("-m", "--message", help="mensaje esteganografico", required=True)
    parser.add_argument("-t", "--offset", help="offset en pixels del inicio del raster", required=True)
    parser.add_argument("-i", "--interleave", help="interleave de modificacion en pixel", required=True)
    parser.add_argument("-o", "--output", help="estego-mensaje", required=True)

    args = parser.parse_args()

    size = int(args.size)
    archivo = args.file
    mensaje = args.message
    offset = int(args.offset)
    interleave = int(args.interleave)
    output = args.output

    img = []

    try:
        fd = os.open(archivo, os.O_RDONLY)
        while True:
            leido = os.read(fd, size)
            img.append(leido)
            if len(leido) < size:
                print("\n\n\nEND OF FILE!")
                break
        

        r = threading.Thread(target=red, args=("h",))
        g = threading.Thread(target=green, args=("i",))
        b = threading.Thread(target=blue, args=("e",))

        r.start()
        g.start()
        b.start()

        r.join()
        g.join()
        b.join()

        listToStr = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])

        byte_stri = bytes(listToStr, encoding="ISO-8859-1")
        in_test = int.from_bytes(byte_stri, byteorder='big')

        fin = bin(in_test).zfill(8)

        print(fin[15:48])
        pixel = []

        pixel = [fin[i:i+8] for i in range(offset, len(fin)-offset, 8)]

        print(pixel[:3])

        header = check_header(listToStr)
        raster = check_raster(listToStr)

        header_byte = str.encode(header, encoding = "ISO-8859-1")
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")

        comentario = "#UMCOPU2 "+str(offset)+" "+str(interleave)+" "+str(os.stat(mensaje).st_size)+"\n"
        
        comment = str.encode(comentario, encoding = "ISO-8859-1")

        fd_output = os.open(output, os.O_RDWR|os.O_CREAT)
        os.write(fd_output, "P6\n".encode(encoding = "ISO-8859-1"))
        os.write(fd_output, comment)
        os.write(fd_output, header_byte)
        os.write(fd_output, raster_byte)
        os.close(fd_output)

        os.close(fd)


    except FileNotFoundError as err:
        print(err)



def check_header(data):
    header_re = r'(#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n)'
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

def red(letra):
    print("soy red: ", os.getpid())
    global text
    text.append(letra)
    print ("1: ", text)
    barrera.wait()

def green(letra):
    print("soy green: ", os.getpid())
    global text
    text.append(letra)
    print ("2: ", text)
    barrera.wait()


def blue(letra):
    print("soy blue: ", os.getpid())
    global text
    text.append(letra)
    print ("3: ", text)
    barrera.wait()


if __name__ == "__main__":
    tp_2()