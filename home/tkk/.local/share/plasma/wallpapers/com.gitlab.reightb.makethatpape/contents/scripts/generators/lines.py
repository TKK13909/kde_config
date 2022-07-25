 
#!/usr/bin/python
from PIL import Image, ImageDraw
import click
import random
from utils import color_util, util
import operator, math

class lines:
    def print_options(self):
        return [
            util.opt("line-min-size", int, 1, sane_low=1, sane_high=4),
            util.opt("line-max-size", int, 10, sane_low=5, sane_high=15),
            util.opt("num-colors", int, 10, sane_low=5, sane_high=30),
            util.opt("angle", int, 45, sane_low=0, sane_high=360),
            util.opt("color", "color", "random")
        ]
        

    def generate(self, image, options):
        w, h = image.size

        draw = ImageDraw.Draw(image)
        self.color = color_util.hex_to_rgb(self.color)
        colors = []

        image.paste(self.color, [0, 0, w, h])

        for _ in range(self.num_colors):
            colors.append(color_util.random_close(self.color))
        
        self.angle = self.angle % 180

        # basically we need to start the line drawing from different sides of the image depending on the angle
        a = self.angle
        if a >= 0 and a <= 45:
            cx = 0
            cy = 0
        elif a > 45 and a <= 90:
            cx = 0
            cy = 0
        elif a > 90 and a <= 135:
            cx = w
            cy = 0
        elif a > 135:
            cx = w
            cy = 0
        m = max(w, h)
        p1 = (0, -m)
        p2 = (0, m)

        cur = 0
        next_width = random.randrange(self.line_min_size, self.line_max_size)
        while cx <= m*2 and cy <= m*2 and cx >= -m*2 and cy >= -m*2: 
            p1r = ( p1[0]*math.cos(math.radians(self.angle)) - p1[1]*math.sin(math.radians(self.angle)),
                    p1[1]*math.cos(math.radians(self.angle)) - p1[0]*math.sin(math.radians(self.angle)) )
            p2r = ( p2[0]*math.cos(math.radians(self.angle)) - p2[1]*math.sin(math.radians(self.angle)),
                    p2[1]*math.cos(math.radians(self.angle)) - p2[0]*math.sin(math.radians(self.angle)) )

            p1r = util.sum_tuples(p1r, (cx, cy))
            p2r = util.sum_tuples(p2r, (cx, cy))
            
            width = next_width
            next_width = random.randrange(self.line_min_size, self.line_max_size)
            random_color = random.choice(colors)

            draw.line([p1r, p2r], fill=random_color, width=width)


            current_move = width*0.5+next_width*0.5
            current_move *= 0.5
            dx = current_move*math.cos(math.radians(self.angle))
            dy = current_move*math.sin(math.radians(self.angle))

            cx += dx
            cy += dy

            #draw.ellipse((cx-10, cy-10, cx+10, cy+10), fill="red", width=10)

            cur += 1
        print("Generated image in " + str(cur) + " passes")
        return image