import socketserver as ss
import os

class Handler(ss.BaseRequestHandler):
    def handle(self):
        dic = {
            "txt":"text/plain",
            "jpg":"image/jpeg",
            "ppm":"image/x-portable-pixmap",
            "html":"text/html",
            "pdf":"application/pdf"
        }
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().splitlines()[0]
        archivo = "." + encabezado.split()[1]

        if archivo == './':
            archivo = './index.html'

        extension = archivo.split('.')[2]
        print(self.client_address)
        print(self.data)

        if os.path.isfile(archivo) == False: #si no esta el archivo
            archivo = './400error.html'

        fd = os.open(archivo, os.O_RDONLY)
        body = os.read(fd, 50000)

        os.close(fd)

        header = bytearray(
            "HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] +
            "\r\nContent-length:"+str(len(body))+
            "\r\n\r\n",'utf8')
            
        self.request.sendall(header)
        self.request.sendall(body)

ss.TCPServer.allow_reuse_address = True
server =  ss.TCPServer(("0.0.0.0", 5000), Handler)
server.serve_forever()