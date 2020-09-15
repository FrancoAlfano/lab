import socket
from threading import Thread
import signal

def service(s2, addr):
    print(addr)
    sent = s2.recv(1024)
    answer = sent.decode().upper()
    s2.send(str.encode(answer, encoding = "ISO-8859-1"))
    print(sent)
    s2.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5000))
s.listen(1)

while True:
    s2, addr = s.accept()
    hilo = Thread(target=service, args= (s2, addr,))
    hilo.start()
    hilo.join()
    s2.close()