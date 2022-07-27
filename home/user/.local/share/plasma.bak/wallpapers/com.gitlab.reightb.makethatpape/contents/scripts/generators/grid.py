 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
from utils import color_util, util
import random

class grid:
    def print_options(self):
        return [
            util.opt("block-size", int, 70, sane_low=10, sane_high=150),
            util.opt("color-count", int, 4, "# of colors close to the one you picked that will be used in the generation", sane_low=2, sane_high=20),
            util.opt("color", "color", "random"),
        ]
        

    def generate(self, image, options):
        w, h = image.size

        bs = self.block_size
        random_colors = self.color_count

        colors = []
        if self.color == "random":
            self.color = color_util.random_rgb() 
        else:
            self.color = color_util.hex_to_rgb(self.color)
        for _ in range(random_colors):
            colors.append(color_util.random_close(self.color))
        draw = ImageDraw.Draw(image)
        for y in range(int(h/bs)+1):
            for x in range(int(w/bs)+1):
                c = random.choice(colors)
                p1 = (x*bs, y*bs)
                p2 = (bs*x+bs, bs*y+bs)
                draw.rectangle([p1, p2], outline=c, fill=c)

                if y > h or x > w:
                    continue

        return image