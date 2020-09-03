import argparse
import os
import re
import array
import logging
import codecs

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Archivo portador", required=True)
    args = parser.parse_args()
    carrier_path = args.file

    return {
        'carrier_path': carrier_path
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
    
    os.close(fd)
    return ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in img])


def get_header(image):
    cipher = r'(#\w+-C)(\d*)\s*(\d*)\s*(\d*)\s*(\d*)'
    header_re = r'(#\w+)(\d*)\s*(\d*)\s*(\d*)\s*(\d*)'

    check_cipher = re.search(cipher, image)
    if check_cipher is not None:
        header_re = cipher
        cipher = True     

    header = re.search(header_re, image)
    offset = header.group(3)
    interleave = header.group(4)
    l_total = header.group(5)
    
    return {
    'offset': offset,
    'interleave': interleave,
    'l_total': l_total,
    'cipher': cipher
    }

def get_raster(image):
    cipher = r'(#\w+-C)(\d*)\s*(\d*)\s*(\d*)\s*(\d*)'
    normal_raster = r'(P6\n)(#\s*\w*\s*-C\s*\d*\s*\d*\s*\d*\d)|((\d* \d*\n\d*\n))([\s\S]*)'
    cipher_raster = r'(255\s*)([\s\S]*)'

    check_cipher = re.search(cipher, image)
    if check_cipher is not None:
        success = re.search(cipher_raster, image)
        raster = success.group(2)
        return raster

    success = re.search(normal_raster, image)
    raster = success.group(5)
    return raster

def rot13(message):
    codec = "abcdefghijklmnopqrstuvwxyz"
    codec2 = codec + codec

    encrypted_message = ""
    for letter in message:
        index = (codec.find(letter))
        if index >= 0:
            encrypted_message = encrypted_message + codec2[index+13]
        else :
            encrypted_message = encrypted_message + letter
    return encrypted_message

