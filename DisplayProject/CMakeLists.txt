# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "/home/user/git/PicoTelegraphDisplay/pico-sdk")

set(PICO_BOARD pico CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.4.0")
  message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.4.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

project(DisplayProject C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

add_subdirectory(lib/Config)
add_subdirectory(lib/OLED)

include_directories(./lib/Config)
include_directories(./lib/OLED)

# Add executable. Default name is the project name, version 0.1

add_executable(DisplayProject DisplayProject.c )

pico_set_program_name(DisplayProject "DisplayProject")
pico_set_program_version(DisplayProject "0.1")

pico_enable_stdio_uart(DisplayProject 1)
pico_enable_stdio_usb(DisplayProject 0)

# Add the standard library to the build
target_link_libraries(DisplayProject
        pico_stdlib
        hardware_spi
        hardware_i2c
        hardware_pwm
        hardware_adc
        OLED
        Config)

# Add the standard include files to the build
target_include_directories(DisplayProject PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/.. # for our common lwipopts or any other standard includes, if required
)

# Add any user requested libraries
target_link_libraries(DisplayProject
        )

pico_add_extra_outputs(DisplayProject)

