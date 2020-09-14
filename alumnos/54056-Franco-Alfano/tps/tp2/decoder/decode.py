import re
import logging
from helpers import (
    process_image,
    get_header,
    get_raster,
    rot13
)        

def _encode_bin(msg):
    return ''.join(format(ord(x), 'b').zfill(8) for x in msg)
    
def _decode_bin(value):
    int_value = int(value, 2)
    return int_value.to_bytes((int_value.bit_length() + 7) // 8, 'big').decode()
    
def extract_message(file_path, msg_length, offset=0, interleave=0, cipher=False):
    image = process_image(file_path, 100)
    
    raster = get_raster(image)

    values_raster = list(raster)
    
    bytes_offset = offset * 3
    bytes_interleave = (interleave * 3)
    
    bin_msg_length = msg_length * 8
    bin_message = ''
    
    empty_buffer = False
    for i in range(bytes_offset, len(raster), bytes_interleave + 3):
        if empty_buffer:
            break
        for j in range(i, i + 3):
            bin_character = _encode_bin(values_raster[j])
            bin_message += bin_character[-1]
    
            bin_msg_length -= 1
            if bin_msg_length == 0:
                empty_buffer = True
                break
    #if cipher == True:
    #    return rot13(_decode_bin(bin_message))
        
    return _decode_bin(bin_message)