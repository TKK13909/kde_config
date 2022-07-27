 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
from utils import color_util

class plain:
    def generate(self, image, options):
        w, h = image.size

        if "color" in options:
            c = color_util.hex_to_rgb(options["color"])
            c += (255,)
        else:
            c = color_util.random_rgb()

        print(f"Generating with color {c}")
        image.paste(c, [0, 0, w, h])
        

        return image