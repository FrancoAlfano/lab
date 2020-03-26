#Ejercicio 6
my_list = [int(x) for x in input("Ingrese valores divididos con coma: ").split(',')]
my_list.sort(reverse=True)
print(my_list)