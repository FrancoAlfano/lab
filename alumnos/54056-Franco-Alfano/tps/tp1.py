#Trabajo Practico n1

import argparse

def tp_1():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--red", help="Bytes de color rojo")
    parser.add_argument("-g", "--green", help="Bytes de color verde")
    parser.add_argument("-b", "--blue", help="Bytes de color azul")
    parser.add_argument("-s", "--size", help="Bloque la lectura", required=True)
    parser.add_argument("-f", "--file", help="nombre de la imagen", required=True)

    args = parser.parse_args()

    print("el nombre del archivo es:", args.file)
    print("el numero de rojo es:", args.red)
    print("el numero de verde es:", args.green)
    print("el numero de azul es:", args.blue)
    print("el numero de el tamaño es:", args.size)



if __name__ == "__main__":
    tp_1()