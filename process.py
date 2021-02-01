#!/usr/bin/env python

import process_lib as proc
import argparse

import matplotlib
matplotlib.style.use('dark_background')

from time import time

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--img', required=True, help='image to be processed')
    ap.add_argument('--out', default=False, help='name of output file (no extension)')
    ap.add_argument('--neg', action='store_true', help='make negative image')
    ap.add_argument('--grayscale','-gs',action='store_true',help='make grayscale image')
    ap.add_argument('--bnw', action='store_true', help='convert pixels to solely black or white based of cutoff value')
    ap.add_argument('--bnw-cutoff','-bnwc',required=False,default=128.0,type=float)
    ap.add_argument('--blur', action='store_true', help='blur picture')
    ap.add_argument('--reach', type=int, default=None, help='reach of neighbors for blur')
    ap.add_argument('--spotlight', action='store_true', help='make spotlight')
    ap.add_argument('--center', nargs=2, action='append', help='coordinates of center')
    ap.add_argument('--radius', type=int, help='radius of spotlight in pixels')
    ap.add_argument('--brighten', type=int, help='brighten or darken image by given amount')
    ap.add_argument('--alter-colors', nargs=3, action='append', help='change values of individual colors')
    ap.add_argument('--filter', help='apply pre determined filter')
    ap.add_argument('--blur-spotlight', action='store_true', help='use for blurring everything except spotlight')
    ap.add_argument('--draw-point', action='store_true', help='draw point on an image')
    ap.add_argument('--view-img', action='store_true')
    flags=ap.parse_args()

    start=time()
    arr=proc.load_img(flags.img)
    proc.image_info(arr)

    if flags.view_img:
        proc.view_img(arr)

    if flags.neg:
        arr=proc.make_negative(arr)

    if flags.grayscale:
        arr=proc.make_grayscale(arr)

    if flags.bnw:
        arr=proc.make_bnw(arr,cutoff=flags.bnw_cutoff)

    if flags.alter_colors:
        arr=proc.alter_colors(arr, action=flags.alter_colors)

    if flags.filter:
        arr=proc.alter_colors(arr, style=flags.filter)

    if flags.blur: 
        arr=proc.blur(arr, flags.reach)

    if flags.spotlight:
        arr=proc.spotlight(arr, flags.center[0], flags.radius)

    if flags.brighten:
        arr=proc.brighten(arr, flags.brighten)

    if flags.blur_spotlight:
        arr=proc.blur_spotlight(arr, flags.center, flags.radius)

    if flags.draw_point:
        arr=proc.draw_point(arr, flags.center, flags.radius)

    print('Process time:\t%g seconds' % round(time()-start,3))

    if flags.out:
        proc.save_image(arr, flags.out)
    else:
        proc.view_img(arr)
    
    
