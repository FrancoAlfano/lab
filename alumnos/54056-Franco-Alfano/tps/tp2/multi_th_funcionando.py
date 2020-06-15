import threading
import time

saldo = 5
barrera = threading.Barrier(3)

def transferencia(monto):
    print ("Thread transf: starting")
    global saldo
    saldo = saldo + monto
    print ("saldo 1", saldo)
    barrera.wait()

def extrae(monto):
    print ("Thread extrae: starting")
    global saldo
    saldo = saldo - monto
    print ("saldo 2", saldo )
    barrera.wait()


def hb(monto):
    print ("Thread hb: starting")
    global saldo
    saldo = saldo - monto
    print ("saldo 3", saldo )
    barrera.wait()


if __name__ == "__main__":
    x = threading.Thread(target=transferencia, args=(5,))
    y = threading.Thread(target=extrae, args=(10,))
    z = threading.Thread(target=hb, args=(10,))
    x.start()
    y.start()
    z.start()
    x.join()
    y.join()
    z.join()
    print ("\nsaldo final ", saldo)
    exit(0)
