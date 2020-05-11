import time
import os
import multiprocessing

start = time.perf_counter()

def do_nothing(qData, qFd):
    print("hola mi nombre es:", os.getpid(), " y mi padre es: ", os.getppid())
    fl = qFd.get()
    data = qData.get()
    for x in range(len(data)):
        os.write(fl, data[x])

    return("done!")


#proc = []
img = []

fd = os.open("dog.ppm", os.O_RDONLY)
fin = os.open("prueba.ppm", os.O_RDWR|os.O_CREAT)

while True:
    leido = os.read(fd, 100)        
    img.append(leido)
    
    if len(leido) < 100:
        print("\n\n\n END OF FILE!")
        break

qData = multiprocessing.Queue()
qFin = multiprocessing.Queue()

qData.put(img)
qFin.put(fin)


#for i in range(3):
proc = multiprocessing.Process(target=do_nothing,args=(qData,qFin,))
proc.start()

#for i in range(3):
proc.join()

os.close(fd)

finish = time.perf_counter()
tt = round(finish-start, 3)
print("tiempo total= ", tt)