#Ejercicio 4
def ejercicio_4():
    my_list = []
    with open('numeros.txt') as f:
        for line in f:
            for i in line:
                if i.isdigit() == True:
                    my_list.append(int(i))
    my_list.sort()

    hist, bin_edges = scipy.histogram([my_list], bins = range(int(my_list[-1])+2))
    plt.bar(bin_edges[:-1], hist, width = 1)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.show()