 
#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFilter
import click
import random
from utils import color_util, util
import operator, math

class gradient:
    def print_options(self):
        return [
            util.opt("line-min-size", int, 2, sane_low=2, sane_high=5),
            util.opt("line-max-size", int, 3, sane_low=6, sane_high=10),
            util.opt("angle", int, 40, sane_low=0, sane_high=360),
            util.opt("color1", "color", "random"),
            util.opt("color2", "color", "random")
        ]
        

    def generate(self, image, options):
        w, h = image.size

        draw = ImageDraw.Draw(image)
        print(self.color1, self.color2)
        self.color1 = color_util.hex_to_rgb(self.color1)
        self.color2 = color_util.hex_to_rgb(self.color2)
        colors = []


        image.paste(self.color1, [0, 0, w, h])

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
        range_x = m*2-cx
        range_y = m*2-cy

        while cx <= m*2 and cy <= m*2 and cx >= -m*2 and cy >= -m*2: 
            p1r = ( p1[0]*math.cos(math.radians(self.angle)) - p1[1]*math.sin(math.radians(self.angle)),
                    p1[1]*math.cos(math.radians(self.angle)) - p1[0]*math.sin(math.radians(self.angle)) )
            p2r = ( p2[0]*math.cos(math.radians(self.angle)) - p2[1]*math.sin(math.radians(self.angle)),
                    p2[1]*math.cos(math.radians(self.angle)) - p2[0]*math.sin(math.radians(self.angle)) )

            p1r = util.sum_tuples(p1r, (cx, cy))
            p2r = util.sum_tuples(p2r, (cx, cy))
            
            width = next_width
            next_width = random.randrange(self.line_min_size, self.line_max_size)
            px = abs(cx)/range_x
            py = abs(cy)/range_y
            random_color = color_util.col_lerp(self.color1, self.color2, px)
            
            draw.line([p1r, p2r], fill=random_color, width=width)


            current_move = width*0.5+next_width*0.5
            current_move *= 0.5
            dx = current_move*math.cos(math.radians(self.angle))
            dy = current_move*math.sin(math.radians(self.angle))

            cx += dx
            cy += dy


            p = math.sqrt(px*px+py*py)

            #draw.ellipse((cx-10, cy-10, cx+10, cy+10), fill="red", width=10)

            cur += 1
        print("Generated image in " + str(cur) + " passes")
        #image = image.filter(ImageFilter.BLUR)
        #image = image.filter(ImageFilter.SMOOTH_MORE)
        return image
