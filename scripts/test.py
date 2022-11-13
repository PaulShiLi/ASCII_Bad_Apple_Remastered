import pygame
from pygame import mixer

mixer.init()
mixer.music.set_volume(0.3)
mixer.music.load('bad_apple.mp3')
mixer.music.play()
