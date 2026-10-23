cmake_minimum_required(VERSION 3.16)
project(logstat LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

file(GLOB_RECURSE LOGSTAT_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

if(NOT LOGSTAT_SOURCES)
    message(FATAL_ERROR "No sources found in src/. Add at least src/main.cpp")
endif()

add_executable(logstat ${LOGSTAT_SOURCES})
target_include_directories(logstat PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_compile_options(logstat PRIVATE -Wall -Wextra -Wpedantic)
