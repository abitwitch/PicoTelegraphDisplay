aux_source_directory(. DIR_UPS_SRCS)

add_library(UPS ${DIR_UPS_SRCS})

target_link_libraries(UPS PUBLIC pico_stdlib hardware_i2c)



