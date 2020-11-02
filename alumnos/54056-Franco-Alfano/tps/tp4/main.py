import asyncio
import os
from async_server import handler
from helpers import parse_arguments

async def main():
    params = parse_arguments()
    directory, port, size= (
        params.get('directory'),
        params.get('port'),
        params.get('size')
    ) 
    dir = directory+"/"
    
    server = await asyncio.start_server(
        lambda reader,address: handler(reader,address,dir,size),
        ('::','0.0.0.0'),port
    )
    async with server:
        await server.serve_forever()
        
asyncio.run(main())
