from PIL import Image

#Read the two images
side1 = Image.open("./models/blocos/minecraft_assets/log_side.png").rotate(270)
side2 = Image.open("./models/blocos/minecraft_assets/log_side.png").rotate(270)
side3 = Image.open("./models/blocos/minecraft_assets/log_side.png").rotate(270)
side4 = Image.open("./models/blocos/minecraft_assets/log_side.png").rotate(270)
top = Image.open("./models/blocos/minecraft_assets/log_top.png").rotate(270)
bot = Image.open("./models/blocos/minecraft_assets/log_top.png").rotate(270)

#resize, first image
new_image = Image.new('RGBA',(64, 64))
new_image.paste(side1,(24,0))
new_image.paste(side2,(24,16))
new_image.paste(side3,(24,32))
new_image.paste(side4,(24,48))
new_image.paste(top,(8,16))
new_image.paste(bot,(40,16))

new_image.save("./models/blocos/log.png","PNG")
new_image.show()