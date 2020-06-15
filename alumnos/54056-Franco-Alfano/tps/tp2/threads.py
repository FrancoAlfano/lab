from concurrent import futures
import os
import time

def red(seg):
   print ("red:", os.getpid())
   time.sleep(seg)
   seg += 1
   return seg

def green(seg):
   print ("green:", os.getpid())
   time.sleep(seg)
   seg += 1
   return seg

def blue(seg):
   print ("blue:", os.getpid())
   time.sleep(seg)
   seg += 1
   return seg

print ("padre:" , os.getpid())
seg = 0
text = "hola mundo"
hilos = futures.ThreadPoolExecutor(max_workers=1)
retornos_futuros = hilos.submit(red,seg)
print (retornos_futuros)
for r in futures.as_completed(retornos_futuros):
    print (r.result())

