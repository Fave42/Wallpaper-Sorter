#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""

@Author: Fabian Fey
"""

import os
from logzero import logger

COLORPATH = '/etc/regolith/styles/costum-theme/color'

def ChangeColors(colorsList):
    colors = [
        "#define color_base03    " + colorsList[0],
        "#define color_base02    " + colorsList[1],
        "#define color_base01    " + colorsList[2],
        "#define color_base00    " + colorsList[3],
        "#define color_base0     " + colorsList[4],
        "#define color_base1     #fffb00",
        "#define color_base2     " + colorsList[5],
        "#define color_base3     " + colorsList[6],
        "#define color_yellow    #fffb00",
        "#define color_orange    #fffb00",
        "#define color_red       #fffb00",
        "#define color_magenta   #fffb00",
        "#define color_violet    #fffb00",
        "#define color_blue      #fffb00",
        "#define color_cyan      #fffb00",
        "#define color_green     #fffb00",
    ]
    with open(COLORPATH, 'w') as colorFile:
        logger.info("Updating color file.")
        for line in colors:
            colorFile.write(line + "\n")


def SetWallpaper(path, file):
    wallpaper = path + "/" + file
    logger.info("Updating wallpaper.")
    command = 'feh --bg-max "' + wallpaper + '"'
    os.system(command)


def ResetI3():
    logger.info("Resetting i3")
    os.system('xrdb -merge ~/.Xresources-regolith && i3 reload')
    