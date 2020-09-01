from concurrent import futures
import os
import time

def tarea(seg, worker):
   print ("worker:", os.getpid()," espero:", seg)
   print("soy worker ", worker)
   time.sleep(seg)
   return seg
   
worker = 0
print ("padre:" , os.getpid())
seg = 0
hilos = futures.ThreadPoolExecutor(max_workers=3)
resultado_a_futuro = hilos.map(tarea,range(3), range(3))
print (list(resultado_a_futuro))
