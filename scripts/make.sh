#!/bin/sh
python script/make.py;
python setup.py sdist bdist_wheel;
