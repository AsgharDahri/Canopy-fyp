import cv2
import numpy as np
import time
from Bridging_Hips_Tracker import bHips
from Left_Roman_Deadlift_Tracker import lRoman
import PoseModule as pm
import xlsxwriter
import math
import json
from json import JSONEncoder
import pandas as pd
from flask import jsonify
from Bicep_Curls_Tracker import gf
from Bent_Over_Reverse_Fly import bentOver
from Bridging_Hips_Tracker import bHips
from Crunches_Legs_Tracker import cLeg
from Left_Roman_Deadlift_Tracker import lRoman
from RussianTwist_Abdominal_Tracker import Rtwist
# from Bicep_Curls_Tracker import success_rate
from flask_cors import CORS
from flask import Flask, render_template, Response
from p import gf1
app = Flask(__name__)
CORS(app)



@app.route('/CLegs')
def video_feed4():
    return Response(cLeg(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
# def index():
    
    # return gf
@app.route('/Rtwist')
def video_feed6():
    return Response(Rtwist(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/lRoman')
def video_feed5():
    return Response(lRoman(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/bHips')
def video_feed3():
    return Response(bHips(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/bentOver')
def video_feed2():
    return Response(bentOver(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(gf(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)