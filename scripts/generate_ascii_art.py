import os
# os.system("pip3 install --user requests")
# os.system("pip3 install Pillow")
# os.system("pip3 install moviepy")
# os.system("pip3 install imageio")
from PIL import Image
import imageio
# os.system("pip3 install imageio-ffmpeg")
# imageio.plugins.ffmpeg.download()
import moviepy
from moviepy.editor import VideoFileClip

video = 'video.mp4'

letter = False
reverse = False
other = True

if letter == True and reverse == False and other == False:
    ASCII_CHARS = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
    ASCII_CHARS = '█▓▒%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
if letter == True and reverse == True and other == False:
    ASCII_CHARS = ' .`\'",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
if letter == False and reverse == False and other == False:
    ASCII_CHARS = ['⠀', '⠄', '⠆', '⠖', '⠶', '⡶', '⣩', '⣪', '⣫', '⣾', '⣿']
if letter == False and reverse == True and other == False:
    ASCII_CHARS = ['⣿', '⣾', '⣫', '⣪', '⣩', '⡶', '⠶', '⠖', '⠆', '⠄', '⠀']
if other == True:
    ASCII_CHARS = ['█', "▓", "▒", '░', '⣫', '⣪', '⣩', '◽', '⠆', '▫', ' ']


def duration(video=video):
    clip = VideoFileClip(video)
    duration = clip.duration
    duration = int(duration)
    return duration


video_length = duration()


def scale_image(image, new_width=100, new_height=30):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    if new_height == 0:
        new_height = int(aspect_ratio * new_width)
    new_image = image.resize((new_width, new_height))
    return new_image


# Discord_version
# def scale_image(image, new_width=60):
#    (old_width, old_height) = image.size
#    aspect_ratio = float(old_height)/float(old_width)
#    new_height = int((aspect_ratio * new_width)/2)
#    new_dim = (new_width, new_height)
#    new_image = image.resize(new_dim)
#    return new_image

def convert_to_grayscale(image):
    return image.convert('L')


def map_pixels_to_ascii_chars(image, range_width=3.69):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    ### Original Symbol ###
    if letter == True and reverse == False:
        pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    if letter == True and reverse == True:
        pixels_to_chars = [ASCII_CHARS[-int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    if letter == False and reverse == False:
        pixels_to_chars = [ASCII_CHARS[pixel_value // 25] for pixel_value in pixels_in_image]
    if letter == False and reverse == True:
        pixels_to_chars = [ASCII_CHARS[-pixel_value // 25] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, new_width=100, new_height=30):
    image = scale_image(image, new_width, new_height)
    #    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)
    image_ascii = [pixels_to_chars[index: index + new_width] for index in
                   range(0, len_pixels_to_chars, new_width)]
    return "\n".join(image_ascii)


def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception:
        print("Unable to open image file {image_filepath}.".format(image_filepath=image_filepath))
    image_ascii = convert_image_to_ascii(image)
    return image_ascii


if __name__ == '__main__':
    import os
    import time
    import cv2

    vidcap = cv2.VideoCapture(video)
    time_count = 0
    frames = []
    while time_count <= video_length * 1000:
        print('Generating ASCII frame at ' + str(time_count))
        vidcap.set(0, time_count)
        success, image = vidcap.read()
        if success:
            cv2.imwrite('output.jpg', image)
        frames.append(handle_image_conversion('output.jpg'))
        time_count = time_count + 100

        # f = open('play.txt', 'w', encoding="cp437")
        f = open('play.txt', 'w', encoding="utf-8")
        f.write('SPLIT'.join(frames))
    f.close()
