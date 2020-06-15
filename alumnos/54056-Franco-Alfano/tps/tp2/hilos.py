from PIL import Image 

i=0
data = "011011000110010101100100011001110110010101110010" #ledger
with Image.open("source.ppm") as img:
    width, height = img.size
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            for n in range(0,3):
                if(i < len(data)):
                    pixel[n] = pixel[n] & ~1 | int(data[i])
                    i+=1
            img.putpixel((x,y), tuple(pixel))
    img.save("source_secret.ppm", "PPM")