#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""

@Author: Fabian Fey
"""

# ToDo: Change the mean color of everything to the mean color of the top most colors
# (this should then only include colors of the same pallette)
# Use clustering:
# https://www.dataquest.io/blog/tutorial-colors-image-clustering-python/

import os
import sys
from logzero import logger

from matplotlib import image as img
from matplotlib import pyplot as plt
import matplotlib

from mpl_toolkits.mplot3d import Axes3D

import pandas as pd

from scipy.cluster.vq import whiten, kmeans

import colorsys
import math

from Changer import ChangeColors, SetWallpaper, ResetI3

CUR_PATH = os.path.dirname(os.path.realpath(__file__))
WALLPAPER_PATH_LINUX = "/home/fabian/Mega/Bilder/Wallpaper"
NUMBERCLUSTERS = 7


def main():
    # ToDo: Add folder input

    for file in os.listdir(WALLPAPER_PATH_LINUX):
            if ".gif" not in file:
                logger.info("Filename: %s", file)
                df = loadPicture(WALLPAPER_PATH_LINUX, file)
                rgbColorsList255, rgbColorsList = clustering(df)
                hexColorsList = rgbToHex(rgbColorsList)
                sorted_hexColorsList = sortColors(hexColorsList)
                
                ChangeColors(sorted_hexColorsList)
                SetWallpaper(WALLPAPER_PATH_LINUX, file)
                ResetI3()

                drawSortedColors(sorted_hexColorsList)
                sys.exit()


def loadPicture(path, file):
    """
    Loads a picture and returnes a pandas dataframe with all pixels devided in RGB values
    """
    image = img.imread(WALLPAPER_PATH_LINUX + '/' + file)

    logger.info("image.shape: %s", image.shape)

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

    df = pd.DataFrame({'red': r, 'blue': b, 'green': g})

    return df


def clustering(df):
    """
    Standardize the variables by dividing each data point by its standard deviation. We will use the whiten() method of the vq class.
    """

    df['scaled_red'] = whiten(df['red'])
    df['scaled_blue'] = whiten(df['blue'])
    df['scaled_green'] = whiten(df['green'])
    df.sample(n = 10)

    # Cluster for 5 colors
    cluster_centers, distortion = kmeans(df[['scaled_red', 'scaled_green', 'scaled_blue']], NUMBERCLUSTERS)

    # print(cluster_centers)

    rgbColorsList = []
    rgbColorsList255 = []
    r_std, g_std, b_std = df[['red', 'green', 'blue']].std()

    for cluster_center in cluster_centers:
        scaled_r, scaled_g, scaled_b = cluster_center
        rgbColorsList255.append((
        math.ceil(scaled_r * r_std),
        math.ceil(scaled_g * g_std),
        math.ceil(scaled_b * b_std)
        ))
        rgbColorsList.append((
        math.ceil(scaled_r * r_std) / 255,
        math.ceil(scaled_g * g_std) / 255,
        math.ceil(scaled_b * b_std) / 255
        ))
    
    logger.info(rgbColorsList)

    return rgbColorsList255, rgbColorsList


def rgbToHex(colorsList):
    """"
    Format RGB to Hex
    colorsList needs to be RGB with 0-1
    """
    hexColors = []
    for color in colorsList:
        hexColors.append(matplotlib.colors.to_hex(color))

    logger.info("hexColors: %s", hexColors)

    return(hexColors)


def sortColors(hexColors):
    def get_hsv(hexrgb):
        # given a color specification in hex RGB, returns its HSV color:
        hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
        r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in range(0,5,2))
        return colorsys.rgb_to_hsv(r, g, b)

    # sort your list of RGB hex colors by hue:
    hexColors.sort(key=get_hsv)
    logger.info("hexColors sorted: %s", hexColors)
    return(hexColors)


def drawSortedColors(sorted_colorsList):
    """
    Format HEX to RGB
    Draw colors
    """
    rgbColors = []
    for color in sorted_colorsList:
        rgbColors.append(matplotlib.colors.to_rgb(color))

    logger.info("rgbColors 0-1: %s", rgbColors)
    
    # fig, axs = plt.subplots(2)
    # axs[0].imshow([rbgColors])
    # axs[1].imshow([sorted_colorsList])
    plt.imshow([rgbColors])
    plt.show()


if __name__ == "__main__":
    main()
