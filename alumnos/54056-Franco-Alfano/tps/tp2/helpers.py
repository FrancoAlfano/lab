import argparse
import os
import re
import array
import logging
import codecs

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="Archivo portador", required=True)
    parser.add_argument("-m", "--message", help="mensaje esteganografico", required=True)
    parser.add_argument("-t", "--offset", help="offset en pixels del inicio del raster", required=True)
    parser.add_argument("-i", "--interleave", help="interleave de modificacion en pixel", required=True)
    parser.add_argument("-o", "--output", help="estego-mensaje", required=True)
    parser.add_argument("-c", "--cipher", help="cifrado adicional", default=False)
    args = parser.parse_args()

    block_size = int(args.size)
    carrier_path = args.file
    message = args.message
    pixels_offset = int(args.offset)
    pixels_interleave = int(args.interleave)
    output_file = args.output
    cipher = bool(args.cipher)

    return {
        'block_size': block_size,
        'carrier_path': carrier_path,
        'message': message,
        'pixels_offset': pixels_offset,
        'pixels_interleave': pixels_interleave,
        'output_file': output_file,
        'cipher': cipher
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
        

def write_image(head, rast, output_file, pixels_offset, pixels_interleave, message, cipher):
    comment_start = "#UMCOMPU2"
    if cipher == True:
        comment_start = "#UMCOMPU2-C"
    comment = "{comment_start} {pixels_offset} {pixels_interleave} {l_total}".format(
        comment_start= comment_start,
        pixels_offset= str(pixels_offset),
        pixels_interleave= str(pixels_interleave),
        l_total= len(message)
    )
    try:
        fd = os.open(output_file, os.O_RDWR|os.O_CREAT)
        header = str.encode(head, encoding = "ISO-8859-1")
        raster = str.encode(rast, encoding = "ISO-8859-1")
        imagen = "P6\n".encode(encoding = "ISO-8859-1") + comment.encode(encoding="ISO-8859-1") + header + raster
        os.write(fd, imagen)
        os.close(fd)

    except FileNotFoundError as err:
        logging.getLogger().error(err)


def _encode_bin(msg):
    return ''.join(format(ord(x), 'b').zfill(8) for x in msg)

def _decode_bin(value):
    int_value = int(value, 2)
    return int_value.to_bytes((int_value.bit_length() + 7) // 8, 'big').decode()
    
def write_message(raster, message, offset=0, interleave=0, cipher=False):
    values_raster = list(raster)

    bytes_offset = offset * 3
    bytes_interleave = (interleave * 3)

    message = check_cipher(cipher, message)

    bin_message = _encode_bin(message)
    pointer = 0


    for i in range(bytes_offset, len(raster), bytes_interleave + 3):
        try:
            for j in range(i, i + 3):
                bin_character = _encode_bin(values_raster[j])
                new_bin_character = '{}{}'.format(bin_character[:-1], bin_message[pointer])
                values_raster[j] = _decode_bin(new_bin_character)
                pointer += 1

        except IndexError:
            pass

    return ''.join(values_raster)

def get_message(message_file):
    with open(message_file, 'r') as file:
        message = file.read()
    return message

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

def check_cipher(cipher, message):
    if cipher == 1:
        message = rot13(message)
    return message



