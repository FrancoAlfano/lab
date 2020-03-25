#Ejercicio 5
def fibo(n,a=0,b=1):
   while n!=0:
      return fibo(n-1,b,a+b)
   return a

for i in range(0,10):
   print(fibo(i))


#Este programa comienza en el for, el cual utiliza range(0,10) lo que significa
#que el for va a interar desde 0 hasta 10, este for va a imprimir lo que 
#devuelva la funcion fibo, que recibe un numero que lo vamos a dar con la variable
#i, la cual va a ir aumentando por cada iteracion del for. Ahora dentro de la funcion
#de fibo tenemos otro iterador, un while, el cual itera siempre y cuando n no sea 0
#si n=0 entonces devuelve a, que en la primera iteracion sera 0.
#Dentro del while vemos el return de fibo: (n-1) en la segunda iteracion sera 0, b =1
#y suma las variables a y b, que en la segunda iteracion dan 1, pero ahora n=0 entonces
#el while es cortado, y fibo devuelve a, el cual en la segunda iteracion es 1, de ahi
#volvemos al for, el cual va recien por la iteracion 2, pasamos a la tercera iteracion
#dentro del while de fibo a la variable a se le suma b mientras que n!=0, restando 1 a n
#en cada iteracion, cuando n=0, nuevamente se devuelve a, ahora sumado b varias veces y
#continua el loop del for hasta completar las 10 iteraciones.