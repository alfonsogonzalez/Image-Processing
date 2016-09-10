#!/usr/bin/env python

import process_lib as proc
import argparse

from time import time

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--img', help='image to be processed')
    ap.add_argument('--out', help='name of output file (no extension)')
    ap.add_argument('--neg', action='store_true', help='make negative image')
    ap.add_argument('--bnw', action='store_true', help='convert to black and white')
    ap.add_argument('--blur', action='store_true', help='blur picture')
    ap.add_argument('--reach', type=int, default=None, help='reach of neighbors for blur')
    ap.add_argument('--spotlight', action='store_true', help='make spotlight')
    ap.add_argument('--center', nargs=2, action='append', help='coordinates of center')
    ap.add_argument('--radius', type=int, help='radius of spotlight in pixels')
    ap.add_argument('--brighten', type=int, help='brighten or darken image by given amount')
    ap.add_argument('--draw-circ', action='store_true', help='draw a cirlce in image')
    ap.add_argument('--alter-colors', nargs=3, action='append', help='change values of individual colors')
    ap.add_argument('--blur-spotlight', action='store_true', help='use for blurring everything except spotlight')
    flags = ap.parse_args()

    start = time()
    arr = proc.load_img(flags.img)

    if flags.neg:
        arr = proc.make_negative(arr)

    if flags.bnw:
        arr = proc.make_bnw(arr)

    if flags.alter_colors:
        arr = proc.alter_colors(arr, flags.alter_colors)

    if flags.blur: 
        arr = proc.blur(arr, flags.reach)

    if flags.spotlight:
        arr = proc.spotlight(arr, flags.center[0], flags.radius)

    if flags.brighten:
        arr = proc.brighten(arr, flags.brighten)

    if flags.blur_spotlight:
        arr = proc.blur_spotlight(arr, flags.center, flags.radius, flags.reach)

    if flags.draw_circ:
        arr = proc.draw_circle(flags.img, flags.center, 55, 60)

    print('Took {} seconds to process'.format((time() - start)))
    proc.save_image(arr, flags.out)
