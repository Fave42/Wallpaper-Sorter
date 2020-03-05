
from PIL import Image  # Pillow
import webcolors

def main():
    im = Image.open('testImage.jpg') # Can be many different formats.
    pix = im.load()

    size = im.size
    length = size[0]
    hight = size[0]

    colorDict = {}
    
    sumRGB = [0, 0, 0]

    for x in range(0, length):
        for y in range(0, hight):
            rgb = pix[x,y]

            sumRGB[0] += rgb[0]
            sumRGB[1] += rgb[1]
            sumRGB[2] += rgb[2]

            if rgb in colorDict:
                colorDict[rgb] += 1
            else:
                colorDict[rgb] = 1

    allPixels = length*hight
    
    avgColor = (int(sumRGB[0]/allPixels), int(sumRGB[1]/allPixels), int(sumRGB[2]/allPixels))
    print(avgColor)

    actualColor, closestColor = get_colour_name(avgColor)

    print("Actual colour name:", actualColor, ", closest colour name:", closestColor)


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


if __name__ == "__main__":
    main()
    # ToDo: Add function to iterate over all wallpapers and sort them by color 