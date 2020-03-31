#Ejercicio 3
import numpy as np
import scipy
import matplotlib.pyplot as plt

def ejercicio_3():
    print("Ingrese numeros, termine con quit: ")
    my_list = []

    while True:
        inp = input()
        if inp == "quit":
            break
        my_list.append(inp)
    print(my_list)
    
    my_list.sort()

    hist, bin_edges = scipy.histogram([my_list], bins = range(int(my_list[-1])+2))
    plt.bar(bin_edges[:-1], hist, width = 1)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.show()


if __name__ == "__main__":
    ejercicio_3()