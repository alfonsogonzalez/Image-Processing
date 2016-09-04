#!/usr/bin/env python

from PIL import Image
from time import time as time
import numpy as np
import argparse

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.near_pix = []

    def avg_colors(self):
        r, g, b = [], [], []
        for pix in self.near_pix:
            r.append(pix.rgb[0])
            g.append(pix.rgb[1])
            b.append(pix.rgb[2])
        return [np.average(r), np.average(g), np.average(b)]

    def dist_from_center(self, center):
        return np.sqrt((self.x - int(center[0]))**2 + (self.y - int(center[1]))**2)

    def scale_values(self, rgbs, scale):
        return [f*scale for f in rgbs]
            
def make_negative(img):
    print('Converting to negative...')
    arr = np.array(Image.open(img))
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            for color in range(arr.shape[2]):
                value = arr[y, x, color]
                if arr[y][x][color] < 127:
                    value += 2*(127 - value)
                    if value > 255:
                        arr[y, x, color] = 255
                    else:
                        arr[y][x][color] += 2*(127 - arr[y][x][color])
                elif arr[y][x][color] > 127:
                    value -= 2*abs((127 - value))
                    if value < 0:
                        #print('too low, value =', value)
                        arr[y, x, color] = 0
                    else:
                        arr[y][x][color] -= 2*(arr[y][x][color] - 127)
    return arr

def avg_values(img, arr=None):
    print('Converting to black and white...')
    if arr is None:
        arr = np.array(Image.open(img))
    else:
        arr = arr
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            avg = np.average(arr[y][x])
            for color in range(arr.shape[2]):
                arr[y][x][color] = avg
    return arr

def make_arr(img, arr=None): #shape is (534, 800, 3)
    master_matrix = []
    row = []
    if arr is None:
        arr = np.array(Image.open(img))
    else:
        arr = arr
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            pix = Pixel(x, y)
            pix.rgb = arr[y][x]
            row.append(pix)
        master_matrix.append(row)
        row = []
    return np.array(master_matrix), arr

def blur(matrix, arr, reach):
    print('Blurring image...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            for i in range(matrix[y][x].x - reach, matrix[y][x].x + reach + 1):
                for j in range(matrix[y][x].y - reach, matrix[y][x].y + reach + 1):
                    try:
                        matrix[y][x].near_pix.append(matrix[j][i])
                    except:
                        pass
            arr[y][x] = matrix[y][x].avg_colors()
    return arr

def spotlight(matrix, arr, center, radius):
    print('Creating spotlight...')
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            dist = matrix[y][x].dist_from_center(center)
            scale = (radius - dist) / radius
            if scale < 0.1:
                scale = 0.1
            arr[y][x] = matrix[y][x].scale_values(arr[y][x], scale)
    return arr

def brighten(img, amount, arr=None):
    print('Altering by:', amount)
    if amount > 0:
        print('Brightening image...')
    else:
        print('Darkening image...')
    if arr is None:
        arr = np.array(Image.open(img))
    else:
        arr = arr
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            for c in range(arr.shape[2]):
                value = arr[y][x][c]
                if amount < 0:
                    if value + amount <= 0:
                        arr[y][x][c] = 0
                    else:
                        arr[y][x][c] += amount
                else:
                    if value + amount >= 255:
                        arr[y][x][c] = 255
                    else:
                        arr[y][x][c] += amount
    return arr

def draw_circle(img, center, inner, outer):
    center_x, center_y = int(center[0][0]), int(center[0][1])
    arr = np.array(Image.open(img))
    for x in range(800):
        for y in range(534):
            if inner < np.sqrt((x - center_x)**2 + (y - center_y)**2) < outer:
                arr[y, x] = np.array([0, 0, 0], dtype=np.uint8)
    return arr
    
     
def save_image(arr, output):
    im = Image.fromarray(arr).save(output)
    print('Image saved to', output)

