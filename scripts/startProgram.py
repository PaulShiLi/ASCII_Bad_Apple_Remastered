import os
import time
from pygame import mixer
from moviepy.editor import VideoFileClip
import platform

operatingSystem = platform.system()


def clear():
    if "windows" in operatingSystem.lower():
        os.system("cls")
    else:
        os.system("clear")


def duration(video_file):
    clip = VideoFileClip(video_file)
    return int(clip.duration)


def convert_video_to_audio_moviepy(video_file, soundPath):
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(f"{soundPath}")


class run:
    rootDir = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered"
    generatedTextDir = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/generated"
    videoPath = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/resources/video.mp4"

    def __init__(self, soundFormat: str = "mp3",
                 playPath: str = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/generated/play.txt",
                 videoPath: str = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/resources/video.mp4", clrScreen: bool = False):
        self.videoPath = videoPath
        self.soundPath = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/resources/video.{soundFormat}"
        self.playPath = playPath
        self.soundFormat = soundFormat
        self.duration = duration(self.videoPath)
        # Create audio file to be played in terminal
        convert_video_to_audio_moviepy(self.videoPath, self.soundPath)
        # Start Frames
        self.showtime(clrScreen)

    def music(self):
        mixer.init()
        mixer.music.set_volume(0.3)
        mixer.music.load(self.soundPath)
        mixer.music.play()

    def showtime(self, clrScreen):
        clear()
        if "windows" in operatingSystem.lower():
            f = open(self.playPath, 'r', encoding="utf-8")
        else:
            f = open(self.playPath, 'r', encoding="cp437")
        frame_raw = f.read()
        frame_raw = frame_raw.replace('.', ' ')
        f.close()
        frames = frame_raw.split('SPLIT')
        for n in range(3):
            print("Starting in", 3 - n)
            time.sleep(1)
        print("Starting in 0")
        self.music()
        init_time = time.time()
        count = 0
        min_count = 0
        sec_count = 0
        while time.time() <= init_time + self.duration:
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
            if clrScreen == True:
                clear()
