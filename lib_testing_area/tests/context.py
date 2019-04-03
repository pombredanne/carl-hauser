# -*- coding: utf-8 -*-

import sys
import os
import pathlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import OpenCV
import ImageHash
import TLSH
import utility_lib.json_class as json_class
import utility_lib.stats_lib as stats_lib
import utility_lib.filesystem_lib  as filesystem_lib
import utility_lib.text_handler  as text_handler
import utility_lib.picture_class  as picture_class

import configuration