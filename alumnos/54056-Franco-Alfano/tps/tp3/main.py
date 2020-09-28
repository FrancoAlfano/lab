from helpers import (
    parse_arguments,
    process_image,
    get_header
)
import socketserver as ss
from sockserver import Handler
from filters import (
    red_img,
    green_img,
    blue_img,
    black_white
)

def main():
    params = parse_arguments()
    directory, port, size= (
        params.get('directory'),
        params.get('port'),
        params.get('size')
    ) 

    ss.ThreadingTCPServer.allow_reuse_address = True
    server =  ss.ThreadingTCPServer(("0.0.0.0", port), Handler)
    server.serve_forever()



if __name__ == "__main__":
    main()