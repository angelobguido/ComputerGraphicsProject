from PIL import Image

top = Image.open("grass_block_side_overlay.png")
back = Image.open("./models/blocos/minecraft_assets/grass_block_side.png")

back.paste(top,(0,0), top)

back.save("grass_block_side.png","PNG")
back.show()