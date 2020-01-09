# unicorn_tools.py

from PIL import Image, ImageDraw, ImageFont
from time import sleep as tsleep
import unicornhathd as uni

_WIDTH, _HEIGHT = uni.get_shape()

_FONT = "/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf"
_FONTSIZE = 12

# Functions for unicornhathd

def set_pixel(x, y, r, g, b) -> None:
    uni.set_pixel(x, y, r, g, b)
    
def set_pixel_hsv(x, y, h, s=1.0, v=1.0) -> None:
    uni.set_pixel_hsv(x, y, h, s, v)

def brightness(b: float) -> None:
    uni.brightness(b)
    
def rotation(r: int) -> None:
    uni.rotation(r)
    
def get_rotation() -> int:
    return uni.get_rotation()
    
def show() -> None:
    uni.show()
    
def clear() -> None:
    uni.clear()
    
def off() -> None:
    uni.off()
    
def get_shape() -> (int, int):
    return uni.get_shape()

# Undocumented functions

def set_all(r, g, b) -> None:
    uni.set_all(r, g, b)

def get_pixels() -> [[[int, int, int]]]:
    return uni.get_pixels()

def shade_pixels(shader) -> None:
    uni.shade_pixels(shader)

# Additional functions

def sleep(n: float) -> None:
    """Avoids importing time in other modules"""
    tsleep(n)

def set_pixels(pixel_list: [[[int, int, int]]]) -> None:
    """Updates the unicorn given the array of colors"""
    for row in range(_HEIGHT):
        for col in range(_WIDTH):
            r, g, b = pixel_list[row][col]
            set_pixel(row, col, r, g, b)

def set_pixel_big(x, y, r, g, b) -> None:
    """Sets a 2x2 area of pixels"""
    x *= 2
    y *= 2
    set_pixel(x,   y,   r, g, b)
    set_pixel(x+1, y,   r, g, b)
    set_pixel(x,   y+1, r, g, b)
    set_pixel(x+1, y+1, r, g, b)

def line_h(x, r, g, b) -> None:
    """Draws a horizontal line at x position"""
    for y in range(_WIDTH):
        set_pixel(x, y, r, g, b)

def line_v(y, r, g, b) -> None:
    """Draws a vertical line at y position"""
    for x in range(_HEIGHT):
        set_pixel(x, y, r, g, b)

def show_letter(s: str, fg: (int)=(255,255,255), bg: (int)=(0,0,0)) -> None:
    """Displays a single character (or more)"""
    font = ImageFont.truetype(_FONT, _FONTSIZE)
    w, h = font.getsize(s)

    image = Image.new("RGB", (_WIDTH, _HEIGHT), bg)
    ImageDraw.Draw(image).text(((_WIDTH-w)/2, (_HEIGHT-h*1.5)/2), s, fg, font)
    image = image.rotate(270) # rotate the image

    for x in range(_WIDTH):
        for y in range(_HEIGHT):
            pixel = image.getpixel((x, y))
            r, g, b = (int(n) for n in pixel)
            set_pixel(-x, y, r, g, b) 
    show()

def show_message(text: str, speed: float=0.02,
                 fg: (int)=(255,255,255), bg: (int)=(0,0,0)) -> None:
    """Displays a scrolling text"""
    old_rotation = get_rotation()
    rotation(old_rotation + 270) # rotate
    
    font = ImageFont.truetype(_FONT, _FONTSIZE)
    w, h = font.getsize(text)

    text_x, text_y = _WIDTH+1, 0

    text_width = w + _WIDTH*3 # padding

    image = Image.new("RGB", (text_width, _HEIGHT), bg)
    ImageDraw.Draw(image).text((text_x, text_y), text, fg, font)

    for scroll in range(text_width - _WIDTH):
        for x in range(_WIDTH):
            for y in range(_HEIGHT):
                pixel = image.getpixel((x + scroll, y))
                r, g, b = (int(n) for n in pixel)
                set_pixel(_WIDTH - 1 - x, y, r, g, b)
        show()
        sleep(speed)
        
    rotation(old_rotation)
    clear()
    show()
