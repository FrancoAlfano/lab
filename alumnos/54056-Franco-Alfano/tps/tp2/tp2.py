#Trabajo Practico n°2

import argparse
import os
import re
import threading
import binascii
import array

text = []
barrera = threading.Barrier(3)

def tp_2():
    
    #BARRIER AL FINAL DE CADA HIJO (3) QUE VALLAN ESCRIBIENDO CADA COLOR Y ESPERANDO 
    #PARA VER QUE BLOQUES HAN SIDO LEIDOS

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
        

        listToStr = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])
        
        mensaje_bin = ''.join(format(ord(x), 'b') for x in mensaje)
        #print(mensaje_bin)

        header = check_header(listToStr)
        raster = check_raster(listToStr)

        byte_stri = b''.join(img)
        in_test = int.from_bytes(byte_stri, byteorder='big')

        fin = bin(in_test).zfill(8)

        #print(fin[15:48])
        pixel = []

        pixel = [fin[i:i+8] for i in range(offset, len(fin)-offset, 8)]
        
        #print(type(pixel[0]))
        header_byte = str.encode(header, encoding = "ISO-8859-1")
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")

        r = threading.Thread(target=red, args=(pixel,mensaje_bin,header_byte))
        g = threading.Thread(target=green, args=(pixel,mensaje_bin,))
        b = threading.Thread(target=blue, args=(pixel,mensaje_bin,))

        r.start()
        g.start()
        b.start()

        #r.join()
        #g.join()
        #b.join()


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

def red(pixel, mensaje_bin, header_byte):
    red = []
    i_red = os.open("red.ppm", os.O_RDWR|os.O_CREAT)
    i = 0
    n = 0
    print(mensaje_bin[0])
    var = str(pixel[0])
    print(var[7])
    for n in pixel[n:len(mensaje_bin):3]:
        lsb = int(var)
        for j in range(0, len(mensaje_bin)):
            if lsb != int(mensaje_bin[j]):
                lsb = int(mensaje_bin[j])
                red.append(pixel[0:6])
                red.append(lsb)
    print(red[0:5])

    if(i < len(mensaje_bin)):
        pixel[n] = int(pixel[n]) & ~1 | int(mensaje_bin[i])
        red.append(pixel[n])
        i+=1

    red = array.array('B',red)
    os.write(i_red, header_byte)
    os.write(i_red, red)
    os.close(i_red)
    barrera.wait()

def green(pixels, mensaje):
    print("soy green: ", os.getpid())
    global text
    text.append(pixels)
    #print ("2: ", text)
    barrera.wait()


def blue(pixels, mensaje):
    print("soy blue: ", os.getpid())
    global text
    text.append(pixels)
    #print ("3: ", text)
    barrera.wait()


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




if __name__ == "__main__":
    tp_2()