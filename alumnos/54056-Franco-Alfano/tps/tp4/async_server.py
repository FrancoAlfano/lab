import helpers
import asyncio
import os

async def handler(reader, address,dir,size):
    data = await reader.read(size)
    req_list = []
    req_list = data.split(b'\r\n')

    #'peername': the remote address to which the socket is connected
    addr = address.get_extra_info('peername')
    log = asyncio.create_task(helpers.log(addr,dir))
    req = asyncio.create_task(answer(req_list,address,dir,size))
    await log, req
    address.close()


async def answer(req_list,writer,dir,size):
    spl_req = req_list[0].decode().split(" ")
    method = spl_req[0]
    file = spl_req[1]

    if(dir == "/"):
    	dir = ""

    if(file != "/"):
        try:
            spl_file = []
            spl_file = file[1:].split(".")
            ext = []
            ext = spl_file[1].split('?')
            if(len(spl_file) == 2):
                extention = spl_file[1]
            else:
                extention = " "
        except:
            file = "/400error.html"
            extention = "html"
            ext = ["html"]
        

    if (file == "/"):
        file = "/index.html"
        extention = "html"
        ext = ["html"]    
    version = str.encode(spl_req[2])

    if(len(ext) > 1):
        send_ok = version + b' 500 Internal Server Error\n'
        writer.write(send_ok)
    else:
        if(method == "POST"):
            send_ok = version + b' 500 Internal Server Error\n'
            writer.write(send_ok)

        elif(method == "GET"):
            file_fd = os.open(dir+file[1:],os.O_RDONLY)
            request = version+b' 200 OK\n'
            content_type = helpers.get_ext(extention)
            request_lenght = b'Content-Lenght:20000\n\n'

            writer.write(request)
            writer.write(bytes(content_type,'utf-8'))
            writer.write(request_lenght)

            reader = os.read(file_fd,size)

            while(reader != b''):
                writer.write(reader)
                reader = os.read(file_fd,size)
            os.close(file_fd)

    await writer.drain()