#!/bin/bash

export LC_ALL=''
export RCM_NO_COLOR=0
export RCM_GRID_ENV=0


cd build
rm -rf lib
mkdir lib

export AKUANDUBA_BASEPATH=`pwd`/..
export LD_LIBRARY_PATH=`pwd`/lib:$LD_LIBRARY_PATH
export PYTHONPATH=`pwd`:$LD_LIBRARY_PATH
export PYTHONPATH=`pwd`/python:$PYTHONPATH
export PATH=`pwd`/scripts:$PATH
cd ..