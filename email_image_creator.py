#!/usr/bin/env python

import sys,Image,ImageFont,ImageDraw

address=sys.argv[1]
image = Image.new("RGBA", (len(address)*8,13), (255,255,255))
usr_font = ImageFont.truetype("cour.ttf", 13)
d_usr = ImageDraw.Draw(image)
d_usr = d_usr.text((0,0), address,(0,0,0), font=usr_font)
image.save(sys.argv[2])
