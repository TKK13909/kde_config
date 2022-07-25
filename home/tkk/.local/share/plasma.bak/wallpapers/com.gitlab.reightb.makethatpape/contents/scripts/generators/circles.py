 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
import random
from utils import color_util, util
import operator, math

class circles:
    def print_options(self):
        return [
            util.opt("color", "color", "random"),
            util.opt("radius", int, 60, sane_low=30, sane_high=200),
            util.opt("iterations", int, 3, sane_low=1, sane_high=3),
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
        i = self.iterations
        for c in range(i):
            for y in range(int(h/r)):
                for x in range(int(w/r)):
                    pts = ((x*r+(c*r*0.5), y*r+(c*r*0.5)), (x*r+r+(c*r*0.5), y*r+r+(c*r*0.5)))
                    draw.ellipse(pts, fill=random.choice(colors))
        return image