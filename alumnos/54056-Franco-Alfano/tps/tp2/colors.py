from threading import Barrier, Thread
from helpers import (
    check_cipher,
    _encode_bin,
    _decode_bin
)

barrera = Barrier(3)
raster = None
msj_size = 0
offset = 0
interleave = 0
cipher = False

def red(message, msj_size):
    write_image(message)
    barrera.wait()

def green(raster, message):
    print("green!")
    barrera.wait()

def blue(raster, message):
    print("blue!")
    barrera.wait()


def rgb_threads(ras, message, off=0, inter=0, ci=False):
    global raster
    global msj_size
    global offset
    global interleave
    global cipher

    raster = ras
    offset = off
    interleave = inter
    cipher = ci
    msj_size = len(message)

    message = check_cipher(cipher, message)

    red_thread = Thread(target=red, args=(message, msj_size))
    green_thread = Thread(target=green, args=(raster, message,))
    blue_thread = Thread(target=blue, args=(raster, message,))

    red_thread.start()
    green_thread.start()
    blue_thread.start()

    return raster


def write_image(message):
    global raster
    global offset
    global interleave
    global cipher

    values_raster = list(raster)

    bytes_offset = offset * 3
    bytes_interleave = (interleave * 3)

    bin_message = _encode_bin(message)
    pointer = 0

    for i in range(bytes_offset, len(raster), bytes_interleave + 3):
        try:
            # Red, Green, Blue
            for j in range(i, i + 3):
                bin_character = _encode_bin(values_raster[j])
                new_bin_character = '{}{}'.format(bin_character[:-1], bin_message[pointer])
                values_raster[j] = _decode_bin(new_bin_character)
                pointer += 1

        except IndexError:
            pass

    raster = ''.join(values_raster)