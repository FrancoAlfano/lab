import socket as s
from threading import Thread
import signal

def service(s2, addr):
    print(addr)
    sent = s2.recv(1024)
    answer = sent.decode().upper()
    s2.send(str.encode(answer, encoding = "ISO-8859-1"))
    print(sent)
    s2.close()

soc = s.socket(s.AF_INET, s.SOCK_STREAM)
soc.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
soc.bind(("127.0.0.1", 5000))
soc.listen(1)

while True:
    s2, addr = soc.accept()
    hilo = Thread(target=service, args= (s2, addr,))
    hilo.start()
    hilo.join()
    s2.close()