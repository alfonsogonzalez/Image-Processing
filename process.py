#!/usr/bin/env python

import process_lib as proc
import argparse

from time import time

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--img', help='image to be processed')
    ap.add_argument('--out', help='name of output file (no extension)')
    ap.add_argument('--neg', action='store_true', help='make negative image')
    ap.add_argument('--avg', action='store_true', help='average pix values')
    ap.add_argument('--blur', action='store_true', help='blur picture')
    ap.add_argument('--reach', type=int, default=None, help='reach of neighbors for blur')
    ap.add_argument('--spotlight', action='store_true', help='make spotlight')
    ap.add_argument('--center', nargs=2, action='append', help='coordinates of center')
    ap.add_argument('--radius', type=int, help='radius of spotlight in pixels')
    ap.add_argument('--brighten', type=int, help='brighten or darken image by given amount')
    ap.add_argument('--draw-circ', action='store_true', help='draw a cirlce in image')
    flags = ap.parse_args()

    start = time()
    second = False
    if flags.neg:
        arr = proc.make_negative(flags.img)
        second = True
    if flags.avg:
        if second:
            arr = proc.avg_values('img', arr=arr)
        else:
            arr = proc.avg_values(flags.img)
        second = True
    if flags.blur:
        if second:
            matrix, array = proc.make_arr('img', arr=arr)
        else:    
            matrix, array = proc.make_arr(flags.img) 
        arr = proc.blur(matrix, array, flags.reach)
    if flags.spotlight:
        if second:
            matrix, array = proc.make_arr('img', arr=arr)
        else:
            matrix, array = proc.make_arr(flags.img)
        arr = proc.spotlight(matrix, array, flags.center[0], flags.radius)
    if flags.brighten:
        if second:
            arr = proc.brighten('img', flags.brighten, arr=arr)
        else:
            arr = proc.brighten(flags.img, flags.brighten)
    if flags.draw_circ:
        arr = proc.draw_circle(flags.img, flags.center, 55, 60)

    print('Took {} seconds to process'.format(time() - start))
    proc.save_image(arr, flags.out)