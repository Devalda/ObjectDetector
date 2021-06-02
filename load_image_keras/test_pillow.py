from PIL import Image
import sys
import base64
import os

print(os.get_exec_path())

IMAGE_NAME = "contoh2.png"

def do_some_stuff(args):
    if len(args) != 2:
        return

    with open(IMAGE_NAME, "wb") as image_file:
        image_file.write(base64.decodebytes(args[1].encode('ascii')))

    image = Image.open(IMAGE_NAME)
    image.show()


if __name__ == 'test_pillow':
    do_some_stuff(sys.argv)


image = Image.open('contoh.png')
image.show()






