from PIL import Image

extracted_bin = []
with Image.open("source_secret.ppm") as img:
    width, height = img.size
    byte = []
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            for n in range(0,3):
                extracted_bin.append(pixel[n]&1)

data = "".join([str(x) for x in extracted_bin])
fin = str.encode(data, encoding = "ISO-8859-1")

print(fin)
