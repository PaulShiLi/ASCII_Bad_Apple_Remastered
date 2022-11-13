import os
import time
from pygame import mixer
import requests
from moviepy.editor import VideoFileClip

video = 'video.mp4'
play = 'play2.txt'


def duration(video=video):
    clip = VideoFileClip(video)
    duration = clip.duration
    duration = int(duration)
    return duration


def music():
    # os.system("open video.mp4")
    data = requests.get(
        "https://github.com/01Sub01/bad_apple/blob/Root/bad_apple.mp3?raw=true"
    )
    with open("bad_apple.mp3", "wb") as f:
        f.write(data.content)
    mixer.init()
    mixer.music.set_volume(0.3)
    mixer.music.load('bad_apple.mp3')
    mixer.music.play()


video_length = duration()


def main():
    # os.system("python3 generate_ascii_art.py")
    os.system("pip3 install moviepy")
    os.system("cls")
    f = open(play, 'r', encoding="cp437")
    frame_raw = f.read()
    frame_raw = frame_raw.replace('.', ' ')
    f.close()
    frames = frame_raw.split('SPLIT')
    for n in range(3):
        print("Starting in", 3 - n)
        time.sleep(1)
    print("Starting in 0")
    music()
    init_time = time.time()
    count = 0
    min_count = 0
    sec_count = 0
    while time.time() <= init_time + video_length:
        print(frames[int((time.time() - init_time) * 10)])
        count += 1
        sec_count += 0.05
        if int(sec_count) < 10:
            # print(f"Frames: {count}  FPS: {round(count/(time.time() - init_time), 2)}  Time: {min_count}:0{int(
            # sec_count)}")
            hold = True
        if int(sec_count) == 60 and int(sec_count) > 10:
            min_count += 1
            sec_count -= 60
        elif int(sec_count) >= 10:
            hold = True
        # print(f"Frames: {count}  FPS: {round(count/(time.time() - init_time), 2)}  Time: {min_count}:{int(
        # sec_count)}")
        time.sleep(0.05)
    os.system('cls')


main()

