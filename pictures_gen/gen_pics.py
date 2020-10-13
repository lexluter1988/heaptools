# stupid starting point
# todo: true random generator
# functions for pixels.
from PIL import Image
import random
import time

imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))

for y in range(imgy):
    for x in range(imgx):
        image.putpixel((x, y), (random.randint(1, 5) % 8 * 32, random.randint(1, 7) % 8 * 32, random.randint(1, 3) % 8 * 32))
image.show()
image.save('my.jpg', 'JPEG')
