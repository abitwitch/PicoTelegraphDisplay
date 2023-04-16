# PicoTelegraphDisplay
A small display unit for a keyboard input. It is specifically designed to pair with the PicoTelegraphKey Repo. 

## Getting started Development 
This should not need to be performed again, but is included for reference. 

1. Install Pico C SDK
    1. `git clone https://github.com/raspberrypi/pico-sdk.git`
    2. `cd pico-sdk`
    3. `git submodule update --init`
    4. `cd ..`
2. Install Toolset
    1. `sudo apt update`
    2. `sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential`
3. Get project generator 
    1. `git clone https://github.com/raspberrypi/pico-project-generator`
    2. `cd pico-project-generator`
    3. `export PICO_SDK_PATH=/home/user/git/PicoTelegraphDisplay/pico-sdk` (or whereever the SDK is located)
    4. `./pico_project.py --gui`
    5. Project Name: "DisplayProject", Location: top folder for this repo
    6. Click OK, then OK

