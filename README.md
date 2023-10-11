# PicoTelegraphDisplay
A small display unit for a keyboard input. It is specifically designed to pair with the PicoTelegraphKey Repo. 

## Hardware Setup
This project uses
- A Raspberry Pi Pico
- Waveshare Display: 2.23inch OLED Display Module for Raspberry Pi Pico (SKU 19750)
- Waveshare UPS: UPS Module for Raspberry Pi Pico, Uninterruptible Power Supply, Li-po Battery, Stackable Design (SKU 20121)
- A Telegraph key of your choosing connected to the 3V3(OUT) and Pin GP21 of the Pico

## Setup
1) Download and install Thonny `sudo apt install thonny`
2) Open Thonny with `sudo thonny`
3) Install MicroPython for the Pico by using the language selector at the bottom left of the thonny window
4) Prepare to upload files ("View" > "Files")
5) Navigate to this repo. Upload the "main.py", and the following folders (and all files in them); "Battery", "SampleText" and "Screen" to the Raspberry Pi Pico

