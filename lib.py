import sys
sys.path.insert(1, '../py-jetanime')
from jetanime import getInfos
import requests
from PIL import Image
from io import BytesIO

def most_frequent_colour(image):

    w, h = image.size
    print(w * h)
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for i in pixels:
        print(i)

    # for count, colour in pixels:
    #     print(count)
    #     if count > most_frequent_pixel[0]:
    #         most_frequent_pixel = (count, colour)

    # compare("Most Common", image, most_frequent_pixel[1])

    return most_frequent_pixel

def average_colour(image):

    colour_tuple = [None, None, None]
    for channel in range(3):

        # Get data for one channel at a time
        pixels = image.getdata(band=channel)

        values = []
        for pixel in pixels:
            values.append(pixel)

        colour_tuple[channel] = sum(values) / len(values)
    for idx, colour in enumerate(colour_tuple):
        colour_tuple[idx] = round(colour)
    colour = int('{:02x}{:02x}{:02x}'.format(*colour_tuple), 16)
    return colour

def average_colour_from_url(image):

    resp = requests.get(image)
    assert resp.ok
    image = Image.open(BytesIO(resp.content))

    colour_tuple = [None, None, None]
    for channel in range(3):

        # Get data for one channel at a time
        pixels = image.getdata(band=channel)

        values = []
        for pixel in pixels:
            values.append(pixel)

        colour_tuple[channel] = sum(values) / len(values)
    for idx, colour in enumerate(colour_tuple):
        colour_tuple[idx] = round(colour)
    colour = int('{:02x}{:02x}{:02x}'.format(*colour_tuple), 16)
    return colour

if __name__ == "__main__":
    url = "https://www.jetanime.cc/startwinkle-precure-48-vostfr/"
    infos = getInfos(url)
    infos = infos.anime()
    image = infos['poster']
    
    print(average_colour_from_url(image))