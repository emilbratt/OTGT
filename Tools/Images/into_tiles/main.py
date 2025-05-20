#!/usr/bin/env python3

# Split PNG image into 4 tiled pieces.
# When you want to print one large image by stitching 4 sheets together.

import sys, os, copy

from PIL import Image

def crop(img: Image, box: (int, int, int, int), new_name: str):
    print(f"Working on {new_name}")
    c = img.crop(box)
    c.save(f"{new_name}.png","PNG")


def main():
    if len(sys.argv) != 2:
        print("pass filename as argument")
        exit(1)

    f = sys.argv[1]
    name, ext = os.path.splitext(f)
    if ext.lower() != ".png":
        print("Only PNG files..")
        exit(1)

    img = Image.open(os.path.join(f))
    w, h = img.size

    top_left = (0, 0, w/2, h/2)
    top_right = (w/2, 0, w, h/2)
    bottom_left = (0, h/2, w/2, h)
    bottom_right = (w/2, h/2, w, h)

    crop(copy.copy(img), top_left, f"{name}_top_left")
    crop(copy.copy(img), top_right, f"{name}_top_right")
    crop(copy.copy(img), bottom_left, f"{name}_bottom_left")
    crop(copy.copy(img), bottom_right, f"{name}_bottom_right")

    print("Done..")

main()