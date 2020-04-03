#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

@Author: Fabian Fey
"""

# ToDo: Change the mean color of everything to the mean color of the top most colors
# (this should then only include colors of the same pallette)
# Use clustering:
# https://www.dataquest.io/blog/tutorial-colors-image-clustering-python/

import os

CUR_PATH = os.path.dirname(os.path.realpath(__file__))
WALLPAPER_PATH_WIN = "D:\MEGA\Bilder\Wallpaper"
# WALLPAPER_PATH_LINUX = "/mnt/d/MEGA/Bilder/Wallpaper"
WALLPAPER_PATH_LINUX = "/home/fabian/Mega/Bilder/Wallpaper"
# WALLPAPER_PATH_WIN = WALLPAPER_PATH_LINUX = os.path.join(CUR_PATH, "test_pics")

from matplotlib import image as img
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

image = img.imread(WALLPAPER_PATH_LINUX + '/Fantasy (129).jpg')

print(image.shape)

# plt.imshow(image)
# plt.show()



# Store all RGB values in lists
r = []
g = []
b = []
for line in image:
    for pixel in line:
        temp_r, temp_g, temp_b = pixel
        r.append(temp_r)
        g.append(temp_g)
        b.append(temp_b)

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter(r, g, b)
# plt.show()

import pandas as pd

df = pd.DataFrame({'red': r, 'blue': b, 'green': g})

# Standardize the variables by dividing each data point by its standard deviation. We will use the whiten() method of the vq class.
from scipy.cluster.vq import whiten

df['scaled_red'] = whiten(df['red'])
df['scaled_blue'] = whiten(df['blue'])
df['scaled_green'] = whiten(df['green'])
df.sample(n = 10)

from scipy.cluster.vq import kmeans

# Cluster for 5 colors
cluster_centers, distortion = kmeans(df[['scaled_red', 'scaled_green', 'scaled_blue']], 16)

# print(cluster_centers)

colors = []
r_std, g_std, b_std = df[['red', 'green', 'blue']].std()

for cluster_center in cluster_centers:
    scaled_r, scaled_g, scaled_b = cluster_center
    colors.append((
    scaled_r * r_std / 255,
    scaled_g * g_std / 255,
    scaled_b * b_std / 255
    ))

# print(colors)
# plt.imshow([colors])
# plt.show()

import math
rbgColors = []
r_std, g_std, b_std = df[['red', 'green', 'blue']].std()

for cluster_center in cluster_centers:
    scaled_r, scaled_g, scaled_b = cluster_center
    rbgColors.append((
    math.ceil(scaled_r * r_std),
    math.ceil(scaled_g * g_std),
    math.ceil(scaled_b * b_std)
    ))

print(rbgColors)

# Format RGB to Hex
import matplotlib
hexColors = []
for color in colors:
    hexColors.append(matplotlib.colors.to_hex(color))

print("hexColors:", hexColors)

import colorsys
def get_hsv(hexrgb):
    # given a color specification in hex RGB, returns its HSV color:
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in range(0,5,2))
    return colorsys.rgb_to_hsv(r, g, b)

# sort your list of RGB hex colors by hue:
hexColors.sort(key=get_hsv)
print("hexColors sorted:", hexColors)

# Format HEX to RGB
rgbColors_sorted = []
for color in hexColors:
    rgbColors_sorted.append(matplotlib.colors.to_rgb(color))

print("rgbColors_sorted 0-1:", rgbColors_sorted)

fig, axs = plt.subplots(2)

axs[0].imshow([rbgColors])
axs[1].imshow([rgbColors_sorted])
plt.show()
