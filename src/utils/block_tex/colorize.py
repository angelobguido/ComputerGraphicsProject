from PIL import Image, ImageChops

img = Image.open("./models/blocos/leaves.png")
color = Image.new('RGBA',(64, 64), (42, 181, 51))

new_image = ImageChops.multiply(img, color)

new_image.save("leaves.png","PNG")
new_image.show()