 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
import random
from utils import color_util, util
import operator

class squares:
    def print_options(self):
        return [
            util.opt("square-min-size", int, 60, sane_low=20, sane_high=60),
            util.opt("square-max-size", int, 200, sane_low=61, sane_high=250),
            util.opt("square-min-width", int, 2, sane_low=2, sane_high=7),
            util.opt("square-max-width", int, 9, sane_low=8, sane_high=20),
            util.opt("num-squares", int, 100, sane_low=50, sane_high=400),
            util.opt("num-colors", int, 10, sane_low=4, sane_high=20),
            util.opt("echoes-min", int, 0, sane_low=0, sane_high=7),
            util.opt("echoes-max", int, 0, sane_low=8, sane_high=20),
            util.opt("color", "color", "random"),
            util.opt("background-color", "color", "random")
        ]
        

    def generate(self, image, options):
        w, h = image.size

        draw = ImageDraw.Draw(image)
        self.color = color_util.hex_to_rgb(self.color)
        colors = []

        image.paste(self.background_color, [0, 0, w, h])

        for _ in range(self.num_colors):
            colors.append(color_util.random_close(self.color))
        for i in range(self.num_squares):
            center = util.random_position(w, h)
            if self.echoes_max-self.echoes_min <= 0:
                echoes = 1
            else:
                echoes = random.randrange(self.echoes_min, self.echoes_max)
            size = random.randrange(self.square_min_size, self.square_max_size)
            width = random.randrange(self.square_min_width, self.square_max_width)
            offset_w = 10 #random.randrange(5, 40)
            dir_x = random.choice([-1, 1, 0.5, -0.5])
            dir_y = random.choice([-1, 1, 0.5, -0.5])
            for j in range(echoes):
                offset = (offset_w*j*dir_x, offset_w*j*dir_y)
                p1 = util.sum_tuples(center, (-size, 0), offset)
                p2 = util.sum_tuples(center, (0, size), offset)
                p3 = util.sum_tuples(center, (size, 0), offset)
                p4 = util.sum_tuples(center, (0, -size), offset)

                points = [p1, p2, p3, p4, p1]
                random_color = random.choice(colors)
                draw.line(points, fill=random_color, width=width)

        return image