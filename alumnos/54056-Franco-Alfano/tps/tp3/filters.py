import os
import logging
from array import array
from helpers import (
    get_header,
    get_raster
)

# By default logging does not print info level messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def red_img(data, header_byte, red_intensity):
    i_red = os.open("red.ppm", os.O_RDWR|os.O_CREAT)
    raster = get_raster(data)
    raster_byte = str.encode(raster, encoding = "ISO-8859-1")
    red = []

    for i in range(0,len(raster_byte),3):
        bit = raster_byte[i]*red_intensity
        if bit > 255:
            bit = 255
        red.append(bit)
        red.append(0)
        red.append(0)  

    red = array('B',red)
    os.write(i_red, header_byte)
    os.write(i_red, red)
    os.close(i_red)
    logger.info('Finished filter red!\n')


def green_img(data, header_byte, gree_intensity):
    i_green = os.open("green.ppm", os.O_RDWR|os.O_CREAT)
    raster = get_raster(data)
    raster_byte = str.encode(raster, encoding = "ISO-8859-1")
    green = []

    for i in range(1,len(raster_byte),3):
        bit = raster_byte[i]*gree_intensity
        if bit > 255:
            bit = 255
        green.append(0)
        green.append(bit)
        green.append(0)   

    green = array('B',green)
    os.write(i_green, header_byte)
    os.write(i_green, green)
    os.close(i_green)
    logger.info('Finished filter green!\n')


def blue_img(data, header_byte, blue_intensity):
    i_blue = os.open("blue.ppm", os.O_RDWR|os.O_CREAT)
    raster = get_raster(data)
    raster_byte = str.encode(raster, encoding = "ISO-8859-1")
    blue = []

    for i in range(2,len(raster_byte),3):
        bit = raster_byte[i]*blue_intensity
        if bit > 255:
            bit = 255
        blue.append(0)
        blue.append(0)   
        blue.append(bit)

    blue = array('B',blue)
    os.write(i_blue, header_byte)
    os.write(i_blue, blue)
    os.close(i_blue)
    logger.info('Finished filter blue!\n')

def black_white(data, header_byte, bw_intensity):
    i_bw = os.open("bw.ppm", os.O_RDWR|os.O_CREAT)
    raster = get_raster(data)
    raster_byte = str.encode(raster, encoding = "ISO-8859-1")
    bw = []
    nums = []
    adds = []

    for i in range(0,len(raster_byte),3):
        bit = raster_byte[i]*bw_intensity
        nums.append(bit)

    composite_list = [nums[x:x+3] for x in range(0, len(nums))]
    for n in composite_list:
        color = int(sum(n)/3)
        if color > 255:
            color = 255
        adds.append(color)

    for j in range(0, len(adds)):
        bw.append(adds[j])
        bw.append(adds[j])
        bw.append(adds[j])

    bw = array('B',bw)
    os.write(i_bw, header_byte)
    os.write(i_bw, bw)
    os.close(i_bw)
    logger.info('Finished filter bw!\n')