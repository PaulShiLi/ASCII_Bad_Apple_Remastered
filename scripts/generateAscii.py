import concurrent.futures
import os
from PIL import Image
from moviepy.editor import VideoFileClip
import time
import cv2
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
import platform
from tqdm import tqdm
# import torch
# import GPUtil
# from numba import jit, cuda
# from skvideo.io import vread


duration = None
int_Duration = None
ASCII_CHARS = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
rootDir = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered"
generatedTextDir = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/generated"
generatedTempDir = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/temp"
videoPath = f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/resources/video.mp4"
config = {'letter': True, 'other': False, 'reverse': False}

operatingSystem = platform.system()


def clear():
    if "windows" in operatingSystem.lower():
        os.system("cls")
    else:
        os.system("clear")


class generateWCPU:
    duration = duration
    int_Duration = int_Duration
    ASCII_CHARS = ASCII_CHARS
    rootDir = rootDir
    generatedTextDir = generatedTextDir
    generatedTempDir = generatedTempDir
    videoPath = videoPath
    threadsEnqueue = None
    overallProgress = None
    trackingProgress = None
    individualProgress = []

    def __init__(self, videoPath: str = videoPath,
                 dimension: str = "0x0",
                 config=config, threadNum=8, debug: bool = True):
        self.newWidth = int(dimension.split("x")[0])
        self.newHeight = int(dimension.split("x")[1])
        self.video = videoPath
        self.config = config
        self.debug = debug
        self.asciiChars(config=config)
        self.duration, self.int_Duration = generateWCPU.duration(self.video)
        self.vidConvert(threadNum)

    def progressBarInit(self):
        trackNum = 0
        for i in range(0, len(self.threadsEnqueue)):
            trackNum += len(self.threadsEnqueue[i])
        self.trackingProgress = tqdm(desc="Overall Completion", colour="GREEN", smoothing=1, unit="frame(s)", total=trackNum)
        self.overallProgress = tqdm(desc="Thread Completion", colour="BLUE", bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} thread(s)', total=len(self.threadsEnqueue))
        for i in range(0, len(self.threadsEnqueue)):
            trackNum += len(self.threadsEnqueue[i])
            self.individualProgress.append(tqdm(desc=f"Thread #{i} Completion", bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} frames [Speed: {rate_fmt}{postfix}]', unit="frame(s)", total=len(self.threadsEnqueue[i])))


    def progressBarUpdate(self, enqueueNum: int, updateType: str):
        if updateType == "thread":
            self.individualProgress[enqueueNum].update(1)
            self.trackingProgress.update(1)
        elif updateType == "overall":
            self.overallProgress.update(1)

    def getEnqueueNum(self, threadEnqueue):
        for i in range(len(self.threadsEnqueue)):
            if self.threadsEnqueue[i] == threadEnqueue:
                return i

    def asciiChars(self, config: dict):
        if config['letter'] == True and config['reverse'] == False and config['other'] == False:
            self.ASCII_CHARS = r'█▓▒%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
        elif config['letter'] == True and config['reverse'] == True and config['other'] == False:
            self.ASCII_CHARS = r' .`\'",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
        elif config['letter'] == False and config['reverse'] == False and config['other'] == False:
            self.ASCII_CHARS = ['⠀', '⠄', '⠆', '⠖', '⠶', '⡶', '⣩', '⣪', '⣫', '⣾', '⣿']
        elif config['letter'] == False and config['reverse'] == True and config['other'] == False:
            self.ASCII_CHARS = ['⣿', '⣾', '⣫', '⣪', '⣩', '⡶', '⠶', '⠖', '⠆', '⠄', '⠀']
        elif config['other'] == True:
            self.ASCII_CHARS = ['█', "▓", "▒", '░', '⣫', '⣪', '⣩', '◽', '⠆', '▫', ' ']

    def duration(video: str):
        clip = VideoFileClip(video)
        duration = clip.duration
        return duration, int(duration)

    def scaleImage(image, newWidth, newHeight):
        (oriWidth, oriHeight) = image.size
        aspectRatio = float(oriHeight) / float(oriWidth)
        aspectRatio_Reversed = float(oriWidth) / float(oriHeight)
        if newHeight == 0 and newWidth != 0:
            newHeight = int(aspectRatio * newWidth)
        elif newHeight == 0 and newWidth == 0:
            newHeight = oriHeight
            newWidth = oriWidth
        elif newHeight != 0 and newWidth == 0:
            newWidth = int(aspectRatio_Reversed * oriWidth)
        newDim = (newWidth, newHeight)
        return image.resize(newDim)

    def convert_to_grayscale(image):
        return image.convert('L')

    def map_pixels_to_ascii_chars(self, image, config: dict, range_width=3.69):
        pixels_in_image = list(image.getdata())
        ### Original Symbol ###
        if config['letter'] == True and config['reverse'] == False:
            pixels_to_chars = [self.ASCII_CHARS[int(pixel_value // 25)] for pixel_value in pixels_in_image]
        if config['letter'] == True and config['reverse'] == True:
            pixels_to_chars = [self.ASCII_CHARS[-int(pixel_value // 25)] for pixel_value in pixels_in_image]
        if config['letter'] == False and config['reverse'] == False:
            pixels_to_chars = [self.ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
        if config['letter'] == False and config['reverse'] == True:
            pixels_to_chars = [self.ASCII_CHARS[-int(pixel_value / range_width)] for pixel_value in pixels_in_image]
        return "".join(pixels_to_chars)

    def convert_image_to_ascii(self, image):
        image = generateWCPU.scaleImage(image, self.newWidth, self.newHeight)
        image = generateWCPU.convert_to_grayscale(image)

        pixels_to_chars = self.map_pixels_to_ascii_chars(image, self.config)
        len_pixels_to_chars = len(pixels_to_chars)
        image_ascii = [pixels_to_chars[index: index + self.newWidth] for index in
                       range(0, len_pixels_to_chars, self.newWidth)]
        return "\n".join(image_ascii)

    def imageConvert(self, imgFile: str):
        image = None
        try:
            image = Image.open(imgFile)
        except Exception:
            print(f"Unable to open image file {imgFile}.")
        return self.convert_image_to_ascii(image)

    def vid2img(self, timeCount: int, videoCapture, threadNum: int):
        if self.debug == True:
            print(f"Generating ASCII frame @ {timeCount}")
        videoCapture.set(0, timeCount)
        success, image = videoCapture.read()
        if success:
            if self.debug == True:
                print(f"Frame @ {timeCount} converted successfuly")
            cv2.imwrite(f"{self.generatedTempDir}/out_frame{timeCount}.jpg", image)
        ASCII = self.imageConvert(f"{self.generatedTempDir}/out_frame{timeCount}.jpg")
        os.remove(f"{self.generatedTempDir}/out_frame{timeCount}.jpg")
        self.progressBarUpdate(threadNum, "thread")
        return (timeCount, ASCII)

    def runTask(self, threadEnqueue):
        videoCapture = cv2.VideoCapture(self.video)
        threadNum = self.getEnqueueNum(threadEnqueue=threadEnqueue)
        taskResult = [self.vid2img(timeCount, videoCapture, threadNum) for timeCount in threadEnqueue]
        self.progressBarUpdate(threadNum, "overall")
        return taskResult

    def framesAssign(self, threadNum):
        threadCounter = 0
        threadsEnqueue = [[] for thread in range(0, threadNum)]
        timeCount = 0
        threads = []
        while timeCount <= self.int_Duration * 1000:
            threadsEnqueue[threadCounter].append(timeCount)
            if self.debug == True:
                print(f"Enqueued time #{timeCount} to thread #{threadCounter}")
            if (threadCounter + 1) == threadNum:
                threadCounter = 0
            else:
                threadCounter += 1
            timeCount += 100
        self.threadsEnqueue = threadsEnqueue
        self.progressBarInit()
        with ThreadPoolExecutor() as executor:
            [threads.append(executor.submit(self.runTask, threadEnqueue)) for threadEnqueue in threadsEnqueue]
            concurrent.futures.wait(threads)
            executor.shutdown()
        return threads

    def vidConvert(self, threadNum):
        framesFutures = self.framesAssign(threadNum=threadNum)
        frames = list(chain(*[future.result() for future in framesFutures]))
        frames.sort(key=lambda i: i[0])
        if "windows" in operatingSystem.lower():
            f = open(f"{self.generatedTextDir}/play.txt", 'w', encoding="utf-8")
        else:
            f = open(f"{self.generatedTextDir}/play.txt", 'w', encoding="cp437")
        f.write('SPLIT'.join([frame for timeCount, frame in frames]))
        f.close()


# class generateWGPU:
#     duration = duration
#     int_Duration = int_Duration
#     ASCII_CHARS = ASCII_CHARS
#     rootDir = rootDir
#     generatedTextDir = generatedTextDir
#     generatedTempDir = generatedTempDir
#     videoPath = videoPath
#
#     def __init__(self, videoPath: str = videoPath,
#                  dimension: str = "100x0",
#                  config={'letter': True, 'other': False, 'reverse': False}, threadNum=8):
#         self.newWidth = int(dimension.split("x")[0])
#         self.newHeight = int(dimension.split("x")[1])
#         self.video = videoPath
#         self.config = config
#         self.checkCUDA()
#         self.asciiChars(config=config)
#         self.duration, self.int_Duration = generateWGPU.duration(self.video)
#         self.test()
#
#     def test(self):
#         try:
#             videoCapture = vread(self.video)
#         except AssertionError:
#             print("FFMPEG not installed!\nInstall it here: https://ffmpeg.org/download.html")
#             exit()
#         [print(frame.shape) for frame in videoCapture]
#
#     def asciiChars(self, config: dict):
#         if config['letter'] == True and config['reverse'] == False and config['other'] == False:
#             self.ASCII_CHARS = r'█▓▒%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
#         elif config['letter'] == True and config['reverse'] == True and config['other'] == False:
#             self.ASCII_CHARS = r' .`\'",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
#         elif config['letter'] == False and config['reverse'] == False and config['other'] == False:
#             self.ASCII_CHARS = ['⠀', '⠄', '⠆', '⠖', '⠶', '⡶', '⣩', '⣪', '⣫', '⣾', '⣿']
#         elif config['letter'] == False and config['reverse'] == True and config['other'] == False:
#             self.ASCII_CHARS = ['⣿', '⣾', '⣫', '⣪', '⣩', '⡶', '⠶', '⠖', '⠆', '⠄', '⠀']
#         elif config['other'] == True:
#             self.ASCII_CHARS = ['█', "▓", "▒", '░', '⣫', '⣪', '⣩', '◽', '⠆', '▫', ' ']
#
#     @jit(target_backend='cuda')
#     def duration(video: str):
#         clip = VideoFileClip(video)
#         duration = clip.duration
#         return duration, int(duration)
#
#     @jit(target_backend='cuda')
#     def scaleImage(image, newWidth, newHeight):
#         (oriWidth, oriHeight) = image.size
#         aspectRatio = float(oriHeight) / float(oriWidth)
#         if newHeight == 0:
#             newHeight = int(aspectRatio * newWidth)
#         newDim = (newWidth, newHeight)
#         return image.resize(newDim)
#
#     @jit(target_backend='cuda')
#     def convert_to_grayscale(image):
#         return image.convert('L')
#
#     def map_pixels_to_ascii_chars(self, image, config: dict, range_width=3.69):
#         pixels_in_image = list(image.getdata())
#         ### Original Symbol ###
#         if config['letter'] == True and config['reverse'] == False:
#             pixels_to_chars = [self.ASCII_CHARS[int(pixel_value // 25)] for pixel_value in pixels_in_image]
#         if config['letter'] == True and config['reverse'] == True:
#             pixels_to_chars = [self.ASCII_CHARS[-int(pixel_value // 25)] for pixel_value in pixels_in_image]
#         if config['letter'] == False and config['reverse'] == False:
#             pixels_to_chars = [self.ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
#         if config['letter'] == False and config['reverse'] == True:
#             pixels_to_chars = [self.ASCII_CHARS[-int(pixel_value / range_width)] for pixel_value in pixels_in_image]
#         return "".join(pixels_to_chars)
#
#     @jit(target_backend='cuda')
#     def convert_image_to_ascii(self, image):
#         image = generateWCPU.scaleImage(image, self.newWidth, self.newHeight)
#         image = generateWCPU.convert_to_grayscale(image)
#
#         pixels_to_chars = self.map_pixels_to_ascii_chars(image, self.config)
#         len_pixels_to_chars = len(pixels_to_chars)
#         image_ascii = [pixels_to_chars[index: index + self.newWidth] for index in
#                        range(0, len_pixels_to_chars, self.newWidth)]
#         return "\n".join(image_ascii)
#
#     def imageConvert(self, imgFile: str):
#         image = None
#         try:
#             image = Image.open(imgFile)
#         except Exception:
#             print(f"Unable to open image file {imgFile}.")
#         return self.convert_image_to_ascii(image)
#
#     def vid2img(self, timeCount: int, videoCapture):
#         print(f"Generating ASCII frame @ {timeCount}")
#         videoCapture.set(0, timeCount)
#         success, image = videoCapture.read()
#         if success:
#             # print(f"Frame @ {timeCount} converted successfuly")
#             cv2.imwrite(f"{self.generatedTempDir}/out_frame{timeCount}.jpg", image)
#         ASCII = self.imageConvert(f"{self.generatedTempDir}/out_frame{timeCount}.jpg")
#         os.remove(f"{self.generatedTempDir}/out_frame{timeCount}.jpg")
#         return (timeCount, ASCII)
#
#     def runTask(self, threadEnqueue):
#         videoCapture = vread(self.video)
#         # print(arg)
#         return [self.vid2img(timeCount, videoCapture) for timeCount in threadEnqueue]
#
#     def framesAssign(self, threadNum):
#         threadCounter = 0
#         threadsEnqueue = [[] for thread in range(0, threadNum)]
#         timeCount = 0
#         threads = []
#         print(threadsEnqueue)
#         while timeCount <= self.int_Duration * 1000:
#             threadsEnqueue[threadCounter].append(timeCount)
#             print(f"Enqueued time #{timeCount} to thread #{threadCounter}")
#             if (threadCounter + 1) == threadNum:
#                 threadCounter = 0
#             else:
#                 threadCounter += 1
#             timeCount += 100
#         with ThreadPoolExecutor() as executor:
#             [threads.append(executor.submit(self.runTask, threadEnqueue)) for threadEnqueue in threadsEnqueue]
#             concurrent.futures.wait(threads)
#             executor.shutdown()
#         return threads
#
#     def vidConvert(self, threadNum):
#         framesFutures = self.framesAssign(threadNum=threadNum)
#         frames = list(chain(*[future.result() for future in framesFutures]))
#         frames.sort(key=lambda i: i[0])
#         if "windows" in operatingSystem.lower():
#             f = open(f"{self.generatedTextDir}/play.txt", 'w', encoding="utf-8")
#         else:
#             f = open(f"{self.generatedTextDir}/play.txt", 'w', encoding="cp437")
#         f.write('SPLIT'.join([frame for timeCount, frame in frames]))
#         f.close()
#
#
#     def checkCUDA(self):
#         try:
#             torch.cuda.get_device_name(0)
#             print(f"Current GPU: {torch.cuda.get_device_name(0)}")
#         except AssertionError:
#             clear()
#             gpuList = [gpu.name for gpu in GPUtil.getGPUs()]
#             for gpu in gpuList:
#                 if "nvidia" in gpu.lower():
#                     os.system("nvidia-smi")
#                     print(f"\nTorch with CUDA not installed!\nPlease install Pytorch with the following CUDA version "
#                           f"above!\nLink: https://developer.nvidia.com/cuda-downloads\n")
#                     print("If you have Anaconda installed:\nInstall Cuda: conda install cuda -c nvidia\nInstall "
#                           "Pytorch: https://pytorch.org/get-started/locally/")
#                     exit()
#             print("GPU processing is not supported on this device's GPU!")
#             exit()
