from helpers import (
    parse_arguments,
    process_image,
    get_header,
    get_raster,
    write_image
)
from validations import validate_params

def main():
    params = parse_arguments()
    path, message, block_size, offset, interleave, output = (
        params.get('carrier_path'),
        params.get('message'),
        int(params.get('block_size')),
        params.get('pixels_offset', 0),
        params.get('pixels_interleave', 0),
        params.get('output_file')
    )
    
    validate_params(path, message, block_size, offset, interleave)
    image = process_image(path, block_size)

    header = get_header(image)
    raster = get_raster(image)

    write_image(header, raster, output, offset, interleave, message)


    

if __name__ == "__main__":
    main()