# Ejercicio 2
def ejercicio_2():
    print("Ingrese 2 numeros separados: ")
    n = input()
    m = input()
    my_list = []
    for x in range(1, m+1):
        print("imprimo esto: ", x, " veces")
        my_list.append(int(str(n)*x))
    
    print(my_list)
    print("El resultado de la suma es: ", sum(my_list))

import numpy as np
import scipy
import matplotlib.pyplot as plt