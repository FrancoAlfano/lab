# Ejercicio 1
def ejercicio_1():
    print("Ingrese un numero: ")
    n = input()
    number_1 = int(str(n)*2)
    number_2 = int(str(n)*3)
    print("El resultado de n + nn + nnn es: ", n + number_1 + number_2)


if __name__ == "__main__":
    ejercicio_1()