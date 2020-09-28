import cgi
import filters
import helpers


form = cgi.FieldStorage()
image =  form.getvalue('image')
color = form.getvalue('filter')
intensity = form.getvalue('intensity')

print(image)

data = helpers.process_image(image, 1024)
header = helpers.get_header(image)

if color == 'R':
    filters.red_img(data, header, intensity)