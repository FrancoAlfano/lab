import threading

barrera = threading.Barrier(3)
text = []

def red(letra):
    global text
    text.append(letra)
    print ("1: ", text)
    barrera.wait()

def green(letra):
    global text
    text.append(letra)
    print ("2: ", text)
    barrera.wait()


def blue(letra):
    global text
    text.append(letra)
    print ("3: ", text)
    barrera.wait()


if __name__ == "__main__":
    x = threading.Thread(target=red, args=("h",))
    z = threading.Thread(target=blue, args=("i",))
    y = threading.Thread(target=green, args=("e",))

    x.start()
    y.start()
    z.start()

    x.join()
    y.join()
    z.join()

    print ("\ntexto final: ", text)