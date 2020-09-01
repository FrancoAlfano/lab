import threading
import time
import array
import os

saldo = 5
barrera = threading.Barrier(3)
texto = b"Hola mi nombre es franco ludovico alfano, me gustaria terminar este tp"
texto2 = b"relr mr nrmbre rs rrarcorlurovrcoralranr, ri rourdlrk rofrnirh rstr tr"
original = []
escondido = []

for letra in texto:
    original.append(letra)

for letra in texto2:
    escondido.append(letra)

#oriToString = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in original])
#escoToString = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in escondido])

global posicion
posicion = 0


def transferencia(fd,fd2):
    print("hola")
    red = []

    sti_ori = array.array('B', original)
    
    os.write(fd2, sti_ori)
    
    for msj in escondido[0::3]:
        red.append(msj)

    original[0::3] = red

    #print("RED: ", original)

    #listToStr = ''.join([(bytes.decode(elem, encoding = "ISO-8859-1")) for elem in original])
        
    #mensaje_bin = str.encode(listToStr, encoding = "ISO-8859-1")
    
    fin = array.array('B', original)
    os.write(fd, fin)
    barrera.wait()

def extrae(fd):
    print(" soy")
    green = texto[1:3]
    print("GREEN: ", green)
    #os.write(fd, texto[1::3])
    barrera.wait()


def hb(fd):
    blue = texto[2:3]
    print("BLUE: ", blue)
    #os.write(fd, texto[2::3])
    print("franco")
    barrera.wait()


if __name__ == "__main__":

    fd = os.open("elpruebita.txt", os.O_CREAT|os.O_RDWR)
    fd2 = os.open("original.txt", os.O_CREAT|os.O_RDWR)   

    x = threading.Thread(target=transferencia, args=(fd,fd2,))
    y = threading.Thread(target=extrae, args=(fd,))
    z = threading.Thread(target=hb, args=(fd,))

    x.start()
    y.start()
    z.start()

    os.close(fd)
    os.close(fd2)

