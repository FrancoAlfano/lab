from helpers import (
    parse_arguments,
    process_image,
    get_header
)
from server import service
from filters import (
    red_img,
    green_img,
    blue_img
)

def main():
    params = parse_arguments()
    directory, port, size, carrier_path, red_intensity= (
        params.get('directory'),
        params.get('port'),
        params.get('size'),
        params.get('carrier_path'),
        params.get('red_intensity')
    )

    #image = process_image(carrier_path, size)
    #header = get_header(image)
    #red_img(image, header, red_intensity)
    #green_img(image, header, red_intensity)
    #blue_img(image, header, red_intensity)

    



if __name__ == "__main__":
    main()