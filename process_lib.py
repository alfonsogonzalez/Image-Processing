#!/usr/bin/env python

from PIL import Image
from time import time as time
import numpy as np
import argparse

class Pixel:
    def __init__(self, x, y, colors=None):
        self.x = x
        self.y = y
        self.colors = colors
        self.near_pix = []

    def conv_neg(self, colors):
        out = []
        for c in colors:
            if c > 127:
                c -= 2*(c - 127)
            else:
                c += 2*(127 - c)
            out.append(c)
        out = np.array(out)
        out[out > 255] = 255
        out[out < 0] = 0
        return out

    def blur(self, arr, reach):
        r, g, b = [], [], []
        for x in range(self.x - reach, self.x + reach):
            for y in range(self.y - reach, self.y + reach):
                try:
                    _r, _g, _b = arr[y, x]
                except:
                    continue
                r.append(_r)
                g.append(_g)
                b.append(_b)
        return [np.average(r), np.average(g), np.average(b)]

    def change_color(self, colors, action): # action = {'r': -20, 'g': 0, 'b': 20}
        r, g, b = colors
        r += action['r']
        g += action['g']
        b += action['b']
        rgb = np.array([r, g, b])
        rgb[rgb > 255] = 255
        rgb[rgb < 0] = 0
        return rgb

    def dist_from_center(self, center):
        return np.sqrt((self.x - int(center[0]))**2 + (self.y - int(center[1]))**2)

    def scale_values(self, rgbs, scale):
        return [f*scale for f in rgbs]
            
def make_negative(arr):
    print('Converting to negative...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            arr[y, x] = Pixel(x, y).conv_neg(arr[y, x, :])
    return arr

def make_bnw(arr):
    print('Converting to black and white...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            avg = arr[y, x, :].mean()
            arr[y, x] = [avg, avg, avg]
    return arr

def blur(arr, reach):
    print('Blurring image...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            arr[y, x] = Pixel(x, y).blur(arr, reach)
    return arr

def spotlight(arr, center, radius):
    print('Creating spotlight...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            pix = Pixel(x, y)
            dist = pix.dist_from_center(center)
            scale = (radius - dist) / radius
            if scale < 0.1:
                scale = 0.1
            arr[y, x] = pix.scale_values(arr[y, x], scale)
    return arr

def brighten(arr, amount):
    print('Altering by:', amount)
    if amount > 0:
        print('Brightening image...')
    else:
        print('Darkening image...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            arr[y, x] = Pixel(x, y).change_color(arr[y, x], {'r': amount, 'g': amount, 'b': amount})
    return arr

def draw_circle(img, center, inner, outer):
    center_x, center_y = int(center[0][0]), int(center[0][1])
    arr = np.array(Image.open(img))
    for x in range(800):
        for y in range(534):
            if inner < np.sqrt((x - center_x)**2 + (y - center_y)**2) < outer:
                arr[y, x] = np.array([0, 0, 0], dtype=np.uint8)
    return arr

def alter_colors(arr, action):
    r, g, b = action[0]
    action = {'r': int(r), 'g': int(g), 'b': int(b)}
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            arr[y, x] = Pixel(x, y).change_color(arr[y, x, :], action)
    return arr

def save_image(arr, output):
    im = Image.fromarray(arr).save(output)
    print('Image saved to', output)

def load_img(img):
    return np.array(Image.open(img))
