hilos = futures.ThreadPoolExecutor(max_workers=6)
#resultado_a_futuro = hilos.map(functools.partial(workers.filter, nombre_archivo,seg),geometria)#mapeo
red = [ hilos.submit(worker_red.filter_red,geometria,nombre_archivo,fd,size,messege,i)  for i in range(1,0,-1)]
green = [ hilos.submit(worker_green.filter_green,geometria,nombre_archivo,fd,size,messege,i)  for i in range(1,0,-1)]
blue = [ hilos.submit(worker_blue.filter_blue,geometria,nombre_archivo,fd,size,messege,i)  for i in range(1,0,-1)]

for r in futures.as_completed(red):
    print (r.result())
for g in futures.as_completed(green):
    print (g.result())
for b in futures.as_completed(blue):
    print (b.result())