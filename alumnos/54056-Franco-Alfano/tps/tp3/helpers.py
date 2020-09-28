from re import search
import argparse
import logging
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directorio donde estan los documentos web", required=True)
    parser.add_argument("-p", "--port", help="Puerto en donde espera conexiones nuevas", required=True)
    parser.add_argument("-s", "--size", help="Bloque de lectura máxima para los documentos", required=True)
    parser.add_argument("-f", "--file", help="Archivo portador", required=True)
    parser.add_argument("-r", "--red", help="Intensidad del color rojo", required=True)
    args = parser.parse_args()

    directory = args.dir
    port = args.port
    size = args.size
    carrier_path = args.file
    red_intensity = args.red
    
    return {
        'directory': directory,
        'port': int(port),
        'size': int(size),
        'carrier_path': carrier_path,
        'red_intensity': int(red_intensity)
    }

def get_header(data):
    header_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))'
    try:
        sucess = search(header_re, data)
        return str.encode(sucess.group(0), encoding = "ISO-8859-1")
    except AttributeError as err:
        logging.getLogger().error("Attribute ERROR: {}".format(err))
        return 0

def get_raster(data):
    try:
        raster_re = r'(P6\n)((#\s*\w*\s*\w*\n\d* \d*\n\d*\n)|(\d* \d*\n\d*\n))([\s\S]*)'
        success = search(raster_re, data)
        return success.group(5)
    except AttributeError as err:
        logging.getLogger().error("Attribute ERROR: {}".format(err))
        return 0

def process_image(carrier_path, block_size):
    img = []
    try:
        fd = os.open(carrier_path, os.O_RDONLY)
        while True:
            buffer_read = os.read(fd, block_size)
            img.append(buffer_read)
            if len(buffer_read) < block_size:
                break
        os.close(fd)

    except FileNotFoundError as err:
        logging.getLogger().error(err)
    
    
    return ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])