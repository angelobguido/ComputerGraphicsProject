from PIL import Image

side1 = Image.open("./models/blocos/minecraft_assets/glass.png").rotate(270)
side2 = Image.open("./models/blocos/minecraft_assets/glass.png").rotate(270)
side3 = Image.open("./models/blocos/minecraft_assets/glass.png").rotate(270)
side4 = Image.open("./models/blocos/minecraft_assets/glass.png").rotate(270)
top = Image.open("./models/blocos/minecraft_assets/glass.png").rotate(270)
bot = Image.open("./models/blocos/minecraft_assets/glass.png").rotate(270)

new_image = Image.new('RGBA',(64, 64))
new_image.paste(side1,(24,0))
new_image.paste(side2,(24,16))
new_image.paste(side3,(24,32))
new_image.paste(side4,(24,48))
new_image.paste(top,(8,16))
new_image.paste(bot,(40,16))

new_image.save("./models/blocos/glass.png","PNG")
new_image.show()