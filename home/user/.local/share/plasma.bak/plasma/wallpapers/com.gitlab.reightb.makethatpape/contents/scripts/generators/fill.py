 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
import random
from utils import color_util, util, draw_util
import operator, math

class fill:
    def print_options(self):
        return [
            util.opt("color", "color", "random"),
            util.opt("angle", int, 45, sane_low=30, sane_high=60),
            util.opt("spacing1", int, 50, sane_low=1, sane_high=70),
            util.opt("spacing2", int, 20, sane_low=60, sane_high=200),
            util.opt("num-colors", int, 10, sane_low=4, sane_high=20),
        ]
        

    def generate(self, image, options):
        w, h = image.size
        w = w*2
        h = h*2

        draw = ImageDraw.Draw(image)
        self.color = color_util.hex_to_rgb(self.color)
        colors = []

        image.paste(self.color, [0, 0, w, h])
        pix = image.load()
        for _ in range(self.num_colors):
            colors.append(color_util.random_close(self.color))
       
        m = max(w, h)*2
        cx = 0
        cy = 0
        a = self.angle
        w = 5
        c1 = random.choice(colors)
        c2 = random.choice(colors)
        c1c = color_util.random_close(color_util.dim(c2, 0.8))

        do_dim = False
        while cx <= m*2 and cy <= m*2 and cx >= -m*2 and cy >= -m*2: 
            cx += self.spacing1; draw_util.draw_line(draw, cx, cy, m, a, c1, w)
            cx += self.spacing2; draw_util.draw_line(draw, cx, cy, m, a, c1, w)

            c2 = color_util.dim(c1c, cx/m) if do_dim else c1c
            draw_util.draw_line(draw, cx-m, cy, m*2, -a, c2, int(w*1.5))
            #draw.line((p1r, p2r), fill="red", width=5)
        
        return image