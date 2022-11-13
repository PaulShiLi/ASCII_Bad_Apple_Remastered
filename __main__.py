from scripts import generateAscii, startProgram, fileInfo
import time
import argparse
import sys
import os
if "/" in str(os.getcwd()):
    sys.path.insert(0, f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/scripts")
if "\\" in str(os.getcwd()):
    sys.path.insert(0, f"{os.getcwd()}\\ASCII_Bad_Apple_Remastered\\scripts")


def generate(videoPath: str, dimension: str,
             config: dict, threadNum: int, gpu: bool = False, debug: bool = False):
    startTime = time.time()
    if gpu == False:
        generateAscii.generateWCPU(videoPath=videoPath, dimension=dimension, config=config, threadNum=threadNum, debug=debug)
    # else:
    #     generateAscii.generateWGPU(videoPath=videoPath, dimension=dimension, config=config, threadNum=threadNum)
    endTime = time.time()
    # print(f"Process finished in {endTime - startTime} seconds")


def showtime(soundFormat: str, playPath: str, videoPath: str, clrScreen: bool):
    startProgram.run(soundFormat=soundFormat, playPath=playPath, videoPath=videoPath, clrScreen=clrScreen)


class parse:
    def read(args):
        argList = [str(args.read[n]) for n in len(args)]
        return argList

    def argSetup():
        # Create Parser Object
        parser = argparse.ArgumentParser(description="ASCII Bad Apple Player")

        # Defining arguments for the parser object
        parser.add_argument("-b", "--build", action='store_true', help="Builds the ASCII frames")
        parser.add_argument("-r", "--run", action='store_true', help="Runs the ASCII frames")
        # Defining arguments for variables
        parser.add_argument("-c", "--config", default={'letter': True, 'other': False, 'reverse': True},
                            help="Include configurations | Default: {'letter': True, 'other': False, 'reverse': False}",
                            type=dict)
        parser.add_argument("-v", "--vidPath", default=f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/resources/video.mp4",
                            help=f"Include custom video path | Default: {os.getcwd()}/ASCII_Bad_Apple_Remastered"
                                 f"/resources/video.mp4", type=str)
        parser.add_argument("-p", "--playPath", default=f"{os.getcwd()}/ASCII_Bad_Apple_Remastered/generated/play.txt",
                            help=f"Include custom ASCII Frame path | Default: {os.getcwd()}"
                                 f"/ASCII_Bad_Apple_Remastered/generated/play.txt", type=str)
        parser.add_argument("-d", "--dimension", default="100x0", help="Include dimension | Default: 0x0", type=str)
        parser.add_argument("-t", "--threads", default=4, help="Number of threads when building ASCII frames | "
                                                               "Default: 4", type=int)
        parser.add_argument("-f", "--soundFormat", default="mp3", help="Sound audio quality when played in terminal | "
                                                                       "Default: mp3", type=str)
        parser.add_argument("-e", "--enableDebug", action='store_true',
                            help="Enables messages to be shown during the build process for debugging")
        parser.add_argument("-cls", "--clearScreen", action='store_true',
                            help="Clears Terminal Screen when playing ASCII")
        parser.add_argument("-g", "--enableGPU", action='store_true',
                            help="(NOT SUPPORTED YET) Enables GPU Processing to speed up building process")

        # parse the arguments from standard input
        args = parser.parse_args()
        # Define Vars
        config = args.config
        vidPath = args.vidPath
        playPath = args.playPath
        dimension = args.dimension
        threads = args.threads
        soundFormat = args.soundFormat
        debug = args.enableDebug
        # Run stuff if necessary
        if args.build == True:
            generate(videoPath=vidPath, dimension=dimension, config=config, threadNum=threads, gpu=False, debug=debug)
        elif args.run == True:
            showtime(soundFormat=soundFormat, playPath=playPath, videoPath=vidPath, clrScreen=args.clearScreen)
        else:
            generate(videoPath=vidPath, dimension=dimension, config=config, threadNum=threads, gpu=False, debug=debug)
            showtime(soundFormat=soundFormat, playPath=playPath, videoPath=vidPath, clrScreen=args.clearScreen)


if __name__ == "__main__":
    parse.argSetup()
