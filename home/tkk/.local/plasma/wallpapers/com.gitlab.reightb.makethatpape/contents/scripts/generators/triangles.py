 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
import random
from utils import color_util, util
import operator, math

class triangles:
    def print_options(self):
        return [
            util.opt("color", "color", "random"),
            util.opt("radius", int, 60, sane_low=30, sane_high=200),
            util.opt("num-colors", int, 10, sane_low=4, sane_high=20),
        ]
        

    def generate(self, image, options):
        w, h = image.size

        draw = ImageDraw.Draw(image)
        self.color = color_util.hex_to_rgb(self.color)
        colors = []

        image.paste(self.color, [0, 0, w, h])
        pix = image.load()
        for _ in range(self.num_colors):
            colors.append(color_util.random_close(self.color))
       
        r = self.radius
        for y in range(int((h+r)/r*2)):
            for x in range(int((w+r)/r*2)):
                xr = x*r/2
                yr = y*r
                r2 = r/2
                if x % 2 == 0:
                    pts = (
                        (xr-r2, yr-r2),
                        (xr+r2, yr-r2),
                        (xr, yr+r2)
                    )
                else:
                    pts = (
                        (xr-r2, yr+r2),
                        (xr+r2, yr+r2),
                        (xr, yr-r2)
                    )
                draw.polygon(pts, fill=random.choice(colors))
        return image