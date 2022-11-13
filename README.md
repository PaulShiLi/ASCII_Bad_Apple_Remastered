# ASCII_Bad_Apple_Remastered

# About this Project

A remastered version of ASCII_bad_apple-master but its more convenient and CLI friendly

This project aims to convert videos of various types of format (default is mp4) to be played in CLI.

# Installation

Installation is fairly simple! Just run the command below to install all necessary python modules needed to run this project.

```bash
pip3 install -r .\ASCII_Bad_Apple_Remastered\requirements.txt
```

# Program Documentation

## Building & Running the program

To build both the ASCII frames and run the ASCII frames w/ music, type:

```bash
python .\ASCII_Bad_Apple_Remastered\ [-c] [-v] [-p] [-d] [-t] [-f] [-cls]
```

### General Flags

```bash
	-h, --help            show this help message and exit
	-b, --build           Builds the ASCII frames
	-r, --run             Runs the ASCII frames
```

More information about each flag are included below

## Building

To only build the frames needed, include the flag ****-b****:

```bash
python .\ASCII_Bad_Apple_Remastered\ -b [-c] [-v] [-d] [-t] [-f] [-e]
```

### Flags

```bash
* = Arg required
type = <argument type>
() = Comments

* type = <dict>
	-c CONFIG, --config CONFIG
                        Include configurations | Default: {'letter': True, 'other': False, 'reverse': False}

* type = <string> (Video path to convert to convert to formatted audio to be played in terminal)
	-v VIDPATH, --vidPath VIDPATH
                        Include custom video path | Default:
                        C:\YOUR_PATH_TO_FOLDER/ASCII_Bad_Apple_Remastered/resources/video.mp4

* type = <string> (widthxheight & 0x0 will retain original video dimensions)
	-d DIMENSION, --dimension DIMENSION
                        Include dimension | Default: 0x0

* type = int (Make sure to not lag out your computer by setting a high value for this one)
	-t THREADS, --threads THREADS
                        Number of threads when building ASCII frames | Default: 4

(Might mess up TQDM)
	-e, --enableDebug     Enables messages to be shown during the build process for debugging

(OpenCV doesn't support GPU acceleration by default so currently working on compiling OpenCV to include GPU acceleration)
	-g, --enableGPU       (NOT SUPPORTED YET) Enables GPU Processing to speed up building process
```

## Running

To only run the program, include the flag ****-r****:

```bash
python .\ASCII_Bad_Apple_Remastered\ -r [-v] [-p] [-f] [-cls]
```

### Flags

```bash
* = Arg required
type = <argument type>
() = Comments

* type = <string> (Video path to convert to convert to formatted audio to be played in terminal)
	-v VIDPATH, --vidPath VIDPATH
                        Include custom video path | Default:
                        C:\YOUR_PATH_TO_FOLDER/ASCII_Bad_Apple_Remastered/resources/video.mp4

* type = <string> (txt path to be played if user has a different location for it)
	-p PLAYPATH, --playPath PLAYPATH
                        Include custom ASCII Frame path | Default:
                        C:\YOUR_PATH_TO_FOLDER/ASCII_Bad_Apple_Remastered/generated/play.txt

* type = <string> (Audio format to be played in terminal which can affect sound quality such as lossless and lossy audio formats)
	-f SOUNDFORMAT, --soundFormat SOUNDFORMAT
                        Sound audio format when played in terminal | Default: mp3

* (Can be a bit laggy based off your OS due to different terminal configurations)
	-cls, --clearScreen   Clears Terminal Screen when playing ASCII
```
