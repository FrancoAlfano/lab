#Ejercicio 6
def ejercicio_6():
    my_list = [int(x) for x in input("Ingrese valores divididos con coma: ").split(',')]
    my_list.sort(reverse=True)
    print(my_list)

if __name__ == "__main__":
    ejercicio_6()