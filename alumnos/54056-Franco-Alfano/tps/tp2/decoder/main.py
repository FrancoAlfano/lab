from decode import extract_message
from helpers import(
    parse_arguments,
    get_header,
    process_image
)

def main():

    params = parse_arguments()
    path = params.get('carrier_path')
    image = process_image(path, 100)

    header = get_header(image)
    offset, interleave, l_total, cipher = (
        header.get('offset'),
        header.get('interleave'),
        header.get('l_total'),
        header.get('cipher')
    )

    print(extract_message(path,int(l_total), int(offset), int(interleave), cipher))


if __name__ == "__main__":
    main()