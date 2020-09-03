from threading import Barrier, Thread
from helpers import write_image

barrera = Barrier(3)
raster = None

def red(raster, message):
    print("red!")
    barrera.wait()

def green(raster, message):
    print("green!")
    barrera.wait()

def blue(raster, message):
    print("blue!")
    barrera.wait()


def rgb_threads(ras, message):
    global raster
    raster = ras
    red_thread = Thread(target=red, args=(raster, message,))
    green_thread = Thread(target=green, args=(raster, message,))
    blue_thread = Thread(target=blue, args=(raster, message,))

    red_thread.start()
    green_thread.start()
    blue_thread.start()

    return "rgb_threads!"