import qrcode
from PIL import Image
qr = qrcode.QRCode(
        version = 1,
        box_size = 16,
        border = 1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
)
data = {
    'first_name' : 'King',
    'last_name' : 'Satyakama'
}
qr.add_data(data)
qr.make(fit=True)

color = "rgba(123,27,208,0.8)"
if color[0:4] == 'rgba':
    rgb_color = eval(color[4:])[0:3]
    hex_color = '#' + '%02x%02x%02x' % rgb_color
else:
    hex_color = color

img = qr.make_image(fill_color=hex_color, back_color="white")
img.save("qrcode.png")

first_image = Image.open("sample-parking-sticker.png")

second_image = Image.open("qrcode.png")

first_image.paste(second_image, (600,400))

first_image.save('result.png')
