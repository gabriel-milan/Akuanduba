cmake_minimum_required(VERSION 2.0)

project(Akuanduba)
include(cmake/InstallAkuandubaFunctions.cmake)
Akuanduba_initialize()
set( Python_ADDITIONAL_VERSIONS 2.7.13 2.7.5)
find_package( PythonInterp REQUIRED)
find_package( PythonLibs REQUIRED)

Akuanduba_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python Akuanduba)