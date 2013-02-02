#!/usr/bin/env python

import argparse,Image,ImageFont,ImageDraw

def main():
        parser = argparse.ArgumentParser(description="Email image creator")
        parser.add_argument('address',metavar="<email address>")
        parser.add_argument('outfile',metavar="<output file>")
        args = parser.parse_args()
        address=args.address
        image = Image.new("RGBA", (len(address)*8,13), (255,255,255))
        usr_font = ImageFont.truetype("cour.ttf", 13)
        d_usr = ImageDraw.Draw(image)
        d_usr = d_usr.text((0,0), address,(0,0,0), font=usr_font)
        image.save(args.outfile)

if __name__ == "__main__":
        main()
