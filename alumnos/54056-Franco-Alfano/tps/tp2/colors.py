from threading import Barrier
from helpers import write_image

barrera = Barrier(3)

def red(raster):
    return "red!"
    #barrera.wait()

def green(raster):
    return "green!"
    #barrera.wait()

def blue(raster):
    return "blue!"
    #barrera.wait()