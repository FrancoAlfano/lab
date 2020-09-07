from threading import Thread, Barrier
from helpers import (
    check_cipher,
    _encode_bin,
    _decode_bin
)

color_red = 'red'
color_green = 'green'
color_blue = 'blue'

colors_offset = {
    color_red: 0,
    color_green: 1,
    color_blue: 2,
}

colors_order = [color_red, color_green, color_blue]

barrera = Barrier(3)

def red(message, raster, offset, interleave):
    write_image(color_red, message, raster, offset, interleave)
    barrera.wait()

def green(message, raster, offset, interleave):
    write_image(color_green, message, raster, offset, interleave)
    barrera.wait()

def blue(message, raster, offset, interleave):
    write_image(color_blue, message, raster, offset, interleave)
    barrera.wait()

def assign_bits_to_colors(bin_message):
    color_groups = {
        color_red: [],
        color_green: [],
        color_blue: [],
    }
    rgb_position = 0

    #Iteramos el bin_message asignandole red, green y blue
    #Por cada bit hasta que tenemos 3 mensajes distintos
    #uno por cada color
    for bit in bin_message:
        color = colors_order[rgb_position]
        color_groups[color].append(bit)
        rgb_position += 1

        if rgb_position == len(colors_order):
            rgb_position = 0
    
    return color_groups

def rgb_threads(raster, message, offset=0, interleave=0, cipher=False):
    message = check_cipher(cipher, message)

    values_raster = list(raster)
    bin_message = _encode_bin(message)
    bits_by_color = assign_bits_to_colors(bin_message)

    #Creamos los hilos para cada color
    red_thread = Thread(target=red, args=(bits_by_color[color_red], values_raster, offset, interleave))
    green_thread = Thread(target=green, args=(bits_by_color[color_green], values_raster, offset, interleave))
    blue_thread = Thread(target=blue, args=(bits_by_color[color_blue], values_raster, offset, interleave))

    red_thread.start()
    green_thread.start()
    blue_thread.start()

    #Esperamos que los hilos terminen para seguir con el padre
    red_thread.join()
    green_thread.join()
    blue_thread.join()

    print('All threads are finished!\n')

    return ''.join(values_raster)


def write_image(color, message_bits, raster, offset, interleave):
    # Offset y Interleave los multiplicamos por 3 porque cada
    #pixel tiene 3 bytes de colores: rojo, verde y azul
    bytes_offset = offset * 3
    bytes_interleave = (interleave * 3)

    color_offset = colors_offset[color]
    pointer = 0

    for i in range(bytes_offset, len(raster), bytes_interleave + 3):
        try:
            bit_position = i + color_offset
            bin_character = _encode_bin(raster[bit_position])
            new_bin_character = '{}{}'.format(bin_character[:-1], message_bits[pointer])
            raster[bit_position] = _decode_bin(new_bin_character)
            pointer += 1

        # Da index error cuando se nos termina el mensaje a escribir
        except IndexError:
            print('Finished thread for {}!\n'.format(color))
            return