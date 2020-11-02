from re import search
import argparse
import logging
import os
import time
from datetime import datetime
import asyncio 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directorio donde estan los documentos web", required=True)
    parser.add_argument("-p", "--port", help="Puerto en donde espera conexiones nuevas", required=True)
    parser.add_argument("-s", "--size", help="Bloque de lectura máxima para los documentos", required=True)
    args = parser.parse_args()
    directory = args.dir
    port = args.port
    size = args.size  
    return {
        'directory': directory,
        'port': int(port),
        'size': int(size)
    }

async def log(addr,dir):
    now = datetime.now()
    log_fd = os.open(dir+"log.txt", os.O_CREAT|os.O_WRONLY|os.O_APPEND)        
    log = "Address: "+addr[0]+" Port: "+str(addr[1])+" Date: "+now.strftime("%d/%m/%Y %H:%M:%S")+"\n"
    os.write(log_fd,bytes(log,"utf-8"))
    os.close(log_fd)

def get_ext(ext):
    extentions={
            "txt": "text/plain",
            "jpg": "image/jpeg",
            "ppm": "image/x-portable-pixmap",
            "html": "text/html",
            "pdf": "application/pdf"
            }
    return extentions[ext]
