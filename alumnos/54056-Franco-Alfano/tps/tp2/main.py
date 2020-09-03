from helpers import (
    parse_arguments,
    process_image,
    get_header,
    get_raster,
    write_image,
    write_message,
    get_message,
    rot13
)
from colors import rgb_threads
from validations import validate_params
from threading import Thread


def main():
    params = parse_arguments()
    block_size, path, message, offset, interleave, output, cipher = (
        int(params.get('block_size')),
        params.get('carrier_path'),
        params.get('message'),
        params.get('pixels_offset', 0),
        params.get('pixels_interleave', 0),
        params.get('output_file'),
        params.get('cipher')
    )

    validate_params(path, message, block_size, offset, interleave)
    image = process_image(path, block_size)
    header = get_header(image)
    raster = get_raster(image)
    message = get_message(message)

    red_raster = rgb_threads(raster, message, offset, interleave, cipher)

    #red_raster = write_message(raster, message, offset, interleave, cipher)

    write_image(header, red_raster, output, offset, interleave, message, cipher)

    

if __name__ == "__main__":
    main()