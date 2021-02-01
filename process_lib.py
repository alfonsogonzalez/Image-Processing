#!/usr/bin/env python

from PIL import Image
from time import time

import numpy as np
import matplotlib.pyplot as plt

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def blur(self, arr, reach):
        if self.y - reach < 0 or self.x - reach < 0:
            return [np.float64(0), np.float64(0), np.float64(0)]
        neigh = arr[self.y-reach:self.y+reach, self.x-reach:self.x+reach]
        return [np.average(neigh[:,:,0]), np.average(neigh[:,:,1]), np.average(neigh[:,:,2])]

    def dist_from_center(self, center):
        return np.sqrt((self.x - int(center[0]))**2 + (self.y - int(center[1]))**2)

def make_negative(arr):
    print('Converting to negative...')
    arr[arr < 127] += 2*(126 - arr[arr < 127])
    arr[arr > 127] -= 2*(arr[arr>127] - 128)
    return arr

def make_grayscale(arr):
    print('Converting to grayscale...')
    avg = arr.mean(axis=2)
    arr[:, :, 0] = avg
    arr[:, :, 1] = avg
    arr[:, :, 2] = avg
    arr = arr.astype(np.uint8)
    return arr

def make_bnw(arr,cutoff):
    print('Converting to black and white...')
    avg=arr.mean(axis=2)

    # matrix of pixel values above and below cutoff
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            if avg[y,x]>=cutoff:
                arr[y,x]=[255,255,255]
            else:
                arr[y,x]=[0,0,0]
    return arr

def blur(arr, reach):
    if reach is None:
        print('Did not input reach, please try again')
        exit()
    print('Blurring image...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            arr[y, x] = Pixel(x, y).blur(arr, reach)
    return arr

def spotlight(arr, center, radius):
    print('Creating spotlight...')
    x, y = np.arange(arr.shape[1]), np.arange(arr.shape[0])[:, np.newaxis]
    dist_arr = np.sqrt((x - int(center[0]))**2 + (y - int(center[1]))**2)
    arr = arr.astype(float)
    arr[:, :, 0] *= (radius - dist_arr) / radius
    arr[:, :, 1] *= (radius - dist_arr) / radius
    arr[:, :, 2] *= (radius - dist_arr) / radius
    arr[arr > 255] = 255
    arr[arr < 0] = 0
    return arr.astype(np.uint8)

def brighten(arr, amount):
    print('Altering by:', amount)
    if amount > 0:
        print('Brightening image...')
    else:
        print('Darkening image...')
    arr = arr.astype(np.uint16)
    arr += amount
    arr[arr > 255] = 255
    arr[arr < 0] = 0
    arr = arr.astype(np.uint8)
    return arr

def draw_circle(img, center, inner, outer):
    center_x, center_y = int(center[0][0]), int(center[0][1])
    arr = np.array(Image.open(img))
    for x in range(800):
        for y in range(534):
            if inner < np.sqrt((x - center_x)**2 + (y - center_y)**2) < outer:
                arr[y, x] = np.array([0, 0, 0], dtype=np.uint8)
    return arr

def draw_point(arr, center, radius):
    center_x, center_y = int(center[0][0]), int(center[0][1])
    arr[center_y-radius:center_y+radius, center_x-radius:center_x+radius] = [0,0,0]
    return arr

def alter_colors(arr, action=None, style=None):
    styles = {
    'midwest': {'r': 1, 'g': 0.5, 'b': 0.2, 'multiply': True},
    }
    if action is not None:
        r, g, b = action[0]
        action = {'r': int(r), 'g': int(g), 'b': int(b), 'multiply': False}
    else:
        action = styles[style]
    arr = arr.astype(float)
    if action['multiply']:
        arr[:, :, 0] *= action['r']
        arr[:, :, 1] *= action['g']
        arr[:, :, 2] *= action['b']
    else:
        arr[:, :, 0] += action['r']
        arr[:, :, 1] += action['g']
        arr[:, :, 2] += action['b']
    arr[arr > 255] = 255
    arr[arr < 0] = 0
    return arr.astype(np.uint8)

def blur_spotlight(arr, center, radius):
    blur = {2: 6, 1.8: 5, 1.6: 4, 1.4: 3, 1.2: 2, 1.0: 1}
    center_x, center_y = float(center[0][0]), float(center[0][1])
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            blur_pix = False
            dist = ((x - center_x)**2 + (y - center_y)**2)**0.5
            for scale in sorted(blur.keys(), reverse=True):
                if dist > (scale*radius):
                    reach = blur[scale]
                    blur_pix = True
                    break
            if blur_pix:
                arr[y, x] = Pixel(x, y).blur(arr, reach)
        if x%100==0:
            print(x)
    return arr

def image_info(arr):
    y,x,pix=arr.shape
    print('Image size:\t%i X %i pixels (%i total pixels)' % (y,x,y*x))

def view_img(arr):
    plt.imshow(arr)
    plt.show()

def save_image(arr, output):
    im = Image.fromarray(arr).save(output)
    print('Output image:\t%s' % output)

def load_img(img):
    print('Input image:\t%s' % img)
    return np.array(Image.open(img))
