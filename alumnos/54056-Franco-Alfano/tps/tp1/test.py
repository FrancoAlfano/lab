import array
import os

# PPM header
width = 256
height = 128
maxval = 255
ppm_header = f'P6 {width} {height} {maxval}\n'

# PPM image data (filled with blue)
image = array.array('B', [0, 255, 0] * width * height)

# Save the PPM image as a binary file
fd = os.open("prueba.ppm", os.O_CREAT|os.O_WRONLY)
os.write(fd, bytearray(ppm_header, "ascii"))
os.write(fd, image)
os.close(fd)
'''

with open('blue_example.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)

'''