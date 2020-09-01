import argparse
import os
import re
import array
import logging

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="Archivo portador", required=True)
    parser.add_argument("-m", "--message", help="mensaje esteganografico", required=True)
    parser.add_argument("-t", "--offset", help="offset en pixels del inicio del raster", required=True)
    parser.add_argument("-i", "--interleave", help="interleave de modificacion en pixel", required=True)
    parser.add_argument("-o", "--output", help="estego-mensaje", required=True)
    args = parser.parse_args()

    block_size = int(args.size)
    carrier_path = args.file
    message = args.message
    pixels_offset = int(args.offset)
    pixels_interleave = int(args.interleave)
    output_file = args.output

    return {
        'block_size': block_size,
        'carrier_path': carrier_path,
        'message': message,
        'pixels_offset': pixels_offset,
        'pixels_interleave': pixels_interleave,
        'output_file': output_file
    }

def process_image(carrier_path, block_size):
    img = []      
    try:
        fd = os.open(carrier_path, os.O_RDONLY)
        while True:
            buffer_read = os.read(fd, block_size)
            img.append(buffer_read)
            if len(buffer_read) < block_size:
                break

    except FileNotFoundError as err:
        logging.getLogger().error(err)
    
    return ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])  


def get_header(image):
    header_re = r'(#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n)'
    try:
        sucess = re.search(header_re, image)
        header = sucess.group(0)
        return header
    except AttributeError as err:
        logging.getLogger().error("Attribute ERROR: {}".format(err))
        return 0


def get_raster(image):
    try:
        raster_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))([\s\S]*)'
        success = re.search(raster_re, image)
        raster = success.group(5)
        return raster
    except AttributeError as err:
        logging.getLogger().error("Attribute ERROR: {}".format(err))
        return 0
        

def write_image(head, rast, output_file, pixels_offset, pixels_interleave, message):
    comment = "#UMCOPU2 {pixels_offset} {pixels_interleave} {l_total}".format(
        pixels_offset= str(pixels_offset),
        pixels_interleave= str(pixels_interleave),
        l_total= str(os.stat(message).st_size)
    )
    try:
        fd = os.open(output_file, os.O_RDWR|os.O_CREAT)
        header = str.encode(head, encoding = "ISO-8859-1")
        raster = str.encode(rast, encoding = "ISO-8859-1")
        imagen = "P6\n".encode(encoding = "ISO-8859-1") + comment.encode(encoding="ISO-8859-1") + header + raster
        os.write(fd, imagen)
        os.close(fd)

    except FileNotFoundError as err:
        print(err)