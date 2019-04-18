#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/user/Documents/capstone-zwave/gr-comparison/python
export PATH=/home/user/Documents/capstone-zwave/gr-comparison/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/user/Documents/capstone-zwave/gr-comparison/build/swig:$PYTHONPATH
/usr/bin/python2 /home/user/Documents/capstone-zwave/gr-comparison/python/qa_comparison_py_f.py 
