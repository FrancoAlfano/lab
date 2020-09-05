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

def red(red_msj):
    color = 0
    write_image(red_msj, color)
    barrera.wait()

def green(green_msj):
    color = 1
    write_image(green_msj, color)
    barrera.wait()

def blue(blue_msj):
    color = 2
    write_image(blue_msj, color)
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
    m = list(message)

    red_msj = m[0::3]
    green_msj = m[1::3]
    blue_msj = m[2::3]

    print("RED: ", red_msj, " GREEN: ", green_msj, " BLUE: ", blue_msj)

    red_thread = Thread(target=red, args=(red_msj,))
    green_thread = Thread(target=green, args=(green_msj,))
    blue_thread = Thread(target=blue, args=(blue_msj,))

    red_thread.start()
    green_thread.start()
    blue_thread.start()

    red_thread.join()
    green_thread.join()
    blue_thread.join()

    raster = ''.join(raster)
    return raster


def write_image(message, color):
    global raster
    global offset
    global interleave

    values_raster = list(raster)

    bytes_offset = offset * 3
    bytes_interleave = (interleave * 3)

    bin_message = _encode_bin(message)
    pointer = 0

    j = 0
    #j = j + color

    for i in range(bytes_offset, len(raster), bytes_interleave + 3):
        try:
            for j in range(i, i + color):
                bin_character = _encode_bin(values_raster[j])
                new_bin_character = '{}{}'.format(bin_character[:-1], bin_message[pointer])
                values_raster[j] = _decode_bin(new_bin_character)
                pointer += 1

        except IndexError:
            pass

    raster = values_raster
    #raster = ''.join(values_raster)