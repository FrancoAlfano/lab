#!/usr/bin/python3
from filters import apply_filter
import socketserver
import os

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        extentions={
            "txt":" text/plain",
            "jpg":" image/jpeg",
            "ppm":" image/x-portable-pixmap",
            "html":" text/html",
            "pdf":" application/pdf"
            }

        self.data = self.request.recv(1024)
        header = self.data.decode().splitlines()[0]
        
        file = "." + header.split()[1]
        if file == './':
            file = './index.html'
        ext = file.split('.')[2]

        test = file.find("ppm")
        print("TEST:  qweqweQWE", test)
        if test > 0:
            image = file.split('&')
            name = image[0].split('=')
            color = image[1].split('=')
            intensity = image[2].split('=')
            reading_block = image[3].split('=')
            apply_filter(name[1], color[1], int(intensity[1]), int(reading_block[1]))
            file = "./index.html"
            ext = file.split('.')[2]
            fd2 = os.open(file, os.O_RDONLY)
            body = os.read(fd2, 50000)
            os.close(fd2)
            header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"
            + extentions[ext] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')

            self.request.sendall(header)
            self.request.sendall(body)

        else:
            print(self.client_address)
            print(self.data)
            if os.path.isfile(file) == False: #si no esta el file
                file = './400error.html'
            fd = os.open(file, os.O_RDONLY)
            body = os.read(fd, 50000)
            os.close(fd)
            header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"
            + extentions[ext] +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')

            self.request.sendall(header)
            self.request.sendall(body)