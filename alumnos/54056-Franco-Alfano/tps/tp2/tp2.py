#Trabajo Practico n°2

import argparse
import os
import re

def tp_2():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="Archivo portador", required=True)
    parser.add_argument("-m", "--message", help="mensaje esteganografico", required=True)
    parser.add_argument("-t", "--offset", help="offset en pixels del inicio del raster", required=True)
    parser.add_argument("-i", "--interleave", help="interleave de modificacion en pixel", required=True)
    parser.add_argument("-o", "--output", help="estego-mensaje", required=True)

    args = parser.parse_args()

    archivo = args.file
    size = int(args.size)
    output = args.output

    #print(args.size, args.file, args.message, args.offset, args.interleave, args.output)

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

        header = check_header(listToStr)
        raster = check_raster(listToStr)

        header_byte = str.encode(header, encoding = "ISO-8859-1")
        raster_byte = str.encode(raster, encoding = "ISO-8859-1")

        comment = str.encode("#UMCOPU2 OFFSET INTERLEAVE L_TOTAL\n", encoding = "ISO-8859-1")

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


if __name__ == "__main__":
    tp_2()