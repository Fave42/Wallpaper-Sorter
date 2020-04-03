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

from PIL import Image  # Pillow
import webcolors

CUR_PATH = os.path.dirname(os.path.realpath(__file__))
WALLPAPER_PATH_WIN = "D:\MEGA\Bilder\Wallpaper"
# WALLPAPER_PATH_LINUX = "/mnt/d/MEGA/Bilder/Wallpaper"
WALLPAPER_PATH_LINUX = "/home/fabian/Mega/Bilder/Wallpaper"
# WALLPAPER_PATH_WIN = WALLPAPER_PATH_LINUX = os.path.join(CUR_PATH, "test_pics")


def main():
    iterateFiles()


def colorProcessing(path, file):
    print(os.path.join(path, file))
    im = Image.open(os.path.join(path, file))

    im = im.convert('RGB')

    pix = im.load()

    size = im.size
    length = size[0]
    hight = size[1]

    colorDict = {}
    
    sumRGB = [0, 0, 0]

    for x in range(0, length):
        for y in range(0, hight):
            rgb = pix[x,y]

            try:
                sumRGB[0] += rgb[0]
                sumRGB[1] += rgb[1]
                sumRGB[2] += rgb[2]
            except Exception as e:
                print(e)
                print(rgb)
                exit()

            if rgb in colorDict:
                colorDict[rgb] += 1
            else:
                colorDict[rgb] = 1

    allPixels = length*hight
    
    avgColor = (int(sumRGB[0]/allPixels), int(sumRGB[1]/allPixels), int(sumRGB[2]/allPixels))
    print(avgColor)

    actualColor, closestColor = get_colour_name(avgColor)

    print("Actual colour name:", actualColor, ", closest colour name:", closestColor)

    newFileName = closestColor + "_colored_" + file
    os.rename(os.path.join(path, file), os.path.join(path, newFileName))
    print("########")


def closest_colour(requested_colour):
    ### https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def iterateFiles():
    """
    Ignores any gifs and already categorized pictures
    """
    try:
        for file in os.listdir(WALLPAPER_PATH_LINUX):
            if ".gif" not in file:
                if "_colored_" not in file:
                    colorProcessing(WALLPAPER_PATH_LINUX, file)
    except:
        for file in os.listdir(WALLPAPER_PATH_WIN):
            if ".gif" not in file:
                if "_colored_" not in file:
                    colorProcessing(WALLPAPER_PATH_WIN, file)


if __name__ == "__main__":
    main()
