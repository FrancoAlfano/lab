import os
from concurrent import futures
import time
import threading

candado = threading.Lock()
barrera = threading.Barrier(4)
texto = "Hola mi nombre es franco ludovico alfano, me gustaria terminar este tp"
tamano = len(texto)
posicion = 0


def red(letra):
    print("worker: ", os.getpid())
    os.write(fd, letra)
    barrera.wait()

def green(letra):
    print("worker: ", os.getpid())
    os.write(fd, letra)
    barrera.wait()

def blue(letra):
    print("worker: ", os.getpid())
    os.write(fd, letra)
    barrera.wait()


if __name__ == "__main__":

    posicion = 0

    fd = os.open("elpruebita.txt", os.O_CREAT|os.O_RDWR)    

    print("padre: ", os.getpid())
    hijo = futures.ThreadPoolExecutor(max_workers = 3)


    hilo3 = hijo.submit(blue(str.encode("franco", encoding = "ISO-8859-1")))
    hilo2 = hijo.submit(green(str.encode("soy", encoding = "ISO-8859-1")))
    hilo1 = hijo.submit(red(str.encode("hola", encoding = "ISO-8859-1")))
    


    fd2 = os.open("elpruebita.txt", os.O_RDONLY)

    leido = os.read(fd2, 50)

    print(leido)

    os.close(fd)
    os.close(fd2)
