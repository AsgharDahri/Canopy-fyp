import cv2
import numpy as np
import time
import PoseModule as pm
import xlsxwriter
import math
import json
from json import JSONEncoder
import pandas as pd



error_already_showing = 0
# IF IT CAN'T RECOGNISE THESE LIBRARIES, GO TO PYTHON INTERPRETER -> AVAILABLE PACKAGES - > install the relevant package

# TO RUN A FILE FOR THE FIRST TIME, IN THE TOP-RIGHT CORNER, RUN -> "Run..." -> SELECT FILE NAME (Crunches_Tracker.py)
def gf1():
    txt_w = 85
    return txt_w