from helpers import (
    parse_arguments,
    process_image,
    get_header,
    get_raster,
    write_image,
    get_message
)
from time import perf_counter
from colors import rgb_threads
from validations import validate_params

start = perf_counter()


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

    raster = rgb_threads(raster, message, offset, interleave, cipher)

    write_image(header, raster, output, offset, interleave, message, cipher)

    finish = perf_counter()
    tt = round(finish-start,3)
    print ("Total time: ",tt)

    

if __name__ == "__main__":
    main()