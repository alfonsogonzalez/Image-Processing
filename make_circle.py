#!/usr/bin/env python

import numpy as np
from PIL import Image

def draw_circle(radius, center_x=400, center_y=267):
    arr = np.empty((534, 800, 3), dtype='uint8')
    for x in range(800):
        for y in range(534):
            if np.sqrt((x - center_x)**2 + (y - center_y)**2) < 250:
                arr[y][x] = [50, 100, 220]
            else:
                arr[y][x] = [0, 0, 0]
    im = Image.fromarray(arr)
    im.save('circle.JPG', 'JPEG')

def outline_circle(img):
    print('Outlining...')
    arr = np.array(Image.open(img))
    new = np.empty((534, 800, 3), dtype='uint8')
    outline_points = []
    for y in range(534):
        for x in range(1, 800):
            if abs(np.average(arr[y][x-1]) - np.average(arr[y][x])) > 15:
                new[y][x] = [255, 255, 255]
                outline_points.append((x, y))
    return outline_points

def fill_circle(img, outline_points):
    print('Filling...')
    filled = np.empty((534, 800, 3), dtype='uint8')
    for y in range(534):
        for x in range(800):
            for point in outline_points:
                if x > 400 and point[0] > 400 and y > 267 and point[1] > 267:
                    if x < point[0] and y < point[1]:
                        filled[y][x] = [255, 255, 255]
                        break
    im = Image.fromarray(filled)
    im.save('filled.JPG')
if __name__ == '__main__':
    outline_points = outline_circle('circle.JPG')
    fill_circle('outlined.JPG', outline_points)
            
            
