import cv2
import numpy as np
import time
import PoseModule as pm
import xlsxwriter
import math

"""  REGARDING SUCCESS RATE, UPDATE THE ERROR_KEEPER'S RESPC. VALUE FOR EACH ERROR """

txt_w = 85
error_already_showing = 0

#IF IT CANT RECOGINSE THESE LIBRARIES, GO TO PYTHON INTERPRETER -> AVAILABLE PACKAGES - > install the relevant package
def cLeg():
        
    print("Crunches_Tracker.py")

    # "Resources/man_performing_bicep_curls_micro.mp4"
    cap = cv2.VideoCapture("Resources/crunches.mp4")

    detector = pm.PoseDetector()
    hh = ""


    error_keeper = [1 for i in range(10)]
    max_count = 4.5
    count = 0
    rep_count_locked = 1

    # 0 = going up, 1 = going down
    dir = 0

    #r = 0

    # 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28

    ''' In the following code, we've defined a 3D array used to store the error report and its details 
        along with a set called my_set that is used to store the reps in which those specific errors were made'''

    arr = np.array( [ '0' for i in range(36) ], dtype=object )

    error_report = arr.reshape(12, 3)

    my_set = [set() for _ in range(12)]

    for i in range(0, len(error_report)):
        error_report[i][1] = 0

    error_report[0][0] = 'Your left shoulder is bent too much'
    error_report[1][0] = 'Your left shoulder is too straight'
    error_report[2][0] = 'Your right shoulder is bent too much'
    error_report[3][0] = 'Your right shoulder is too straight'
    error_report[4][0] = 'Your left elbow is getting too wide'
    error_report[5][0] = 'Your left elbow is bending inwards too much'
    error_report[6][0] = 'Your right elbow is getting too wide'
    error_report[7][0] = 'Your right elbow is bending inwards too much'
    error_report[8][0] = 'Your shoulders & knees are too close'
    error_report[9][0] = 'Your shoulders & knees are too far away '
    error_report[10][0] = 'Don\'t close your knees too much'
    error_report[11][0] = 'Your knees are getting too wide'




    #i = 0
    #j = 0

    #exercise_quality = ""
    #exercise_comment = ""


    def check_angle_error( angle_name, sign, angle_val, my_set_val, message):
        global txt_w, error_already_showing
        if( sign == '<'):
            #print("beep")
            if ( ( angle_name < angle_val ) ):

                if (error_already_showing == 1):
                    txt_w = txt_w + 15

                error_already_showing = 1

                my_set[ my_set_val ].add(str(round(count)))
                error_keeper[round(count)] = 0
                cv2.putText(img, message, (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

        if (sign == '>'):
            # print("beep")
            if ((angle_name > angle_val)):

                if (error_already_showing == 1):
                    txt_w = txt_w + 15

                error_already_showing = 1

                my_set[my_set_val].add(str(round(count)))
                error_keeper[round(count)] = 0

                cv2.putText(img, message, (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )




    # def prnt_err(hh, txt_w):
    #    cv2.putText(img, hh, (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )


    while True:
        success, img = cap.read()

        passed_thru = 0
        # Comment this out when you use the webcam

        # img = cv2.resize( img, (480, 710)) # This is used to resize the video/webcam footage

        # Exercise Monitoring begins here

        # This is used to find all the landmarks in the video
        img = detector.findPose(img, True)  # Set the 2nd param to true if you want to see every single landmark + connection

        # Section A1 starts here: The following code is being used to find the landmarks that we're going to use;
        # your landmarks are prob. diff. from the youtuber's...

        # lmList is used to segment the list into individual frames and store them frame-by-frame in an array
        lmList = detector.findPosition(img, False)  # Set the 2nd param to true if you want to see every single landmark

        #print("\nPoint: ", lmList)



        if len(lmList) != 0:
            ''' Section B1: This is where most of the work is done, 90% of all additions/changes will occur here: '''
            #   This is what we're going to do:
            #   1) we're going to calculate the angle at each landmark w.r.t  to all of its adjacent landmarks,
            #   2) then use if-else statements to set initial, final positions etc after identifying primary angles
            #   3) then set conditions on secondary angles to make sure the user performs them correctly

            #  Params: SRC, Point1, Center Point/Point2, Point3, Show Angle or not?
            #angle = detector.findAngle(img, 11, 13, 15, 1)

            #Use the following angles, if needed, create a new one or change landmarks:
            # Angle naming convention: angle_centrepoint_subcat

            #angle_11_a = detector.findAngle(img, 12, 11, 13, 1)
            angle_11_b = detector.findAngle(img, 13, 11, 23, 0)

            #angle_12_a = detector.findAngle(img, 11, 12, 14, 1)
            angle_12_b = detector.findAngle(img, 14, 12, 24, 0)

            angle_13_a = detector.findAngle(img, 11, 13, 15, 0)

            angle_14_a = detector.findAngle(img, 12, 14, 16, 0)

            #angle_15_a = detector.findAngle(img, 13, 15, 19, 1)
            #angle_15_b = detector.findAngle(img, 13, 15, 17, 1)

            #angle_16_a = detector.findAngle(img, 14, 16, 20, 1)
            #angle_16_b = detector.findAngle(img, 14, 16, 18, 1)

            angle_23_a = detector.findAngle(img, 11, 23, 25, 0)

            angle_24_a = detector.findAngle(img, 12, 24, 26, 0)

            angle_25_a = detector.findAngle(img, 23, 25, 27, 0) # P

            angle_26_a = detector.findAngle(img, 24, 26, 28, 0) # P

            #angle_27_a = detector.findAngle(img, 25, 27, 31, 1)
            #angle_27_b = detector.findAngle(img, 25, 27, 29, 1)

            #angle_28_a = detector.findAngle(img, 26, 28, 32, 1)
            #angle_28_b = detector.findAngle(img, 26, 28, 30, 1)s

            ''' Section B2: Do the following:
                1) Calculate/convert the primary angles into percentage values.
                2) Find & set the app. initial/final/inter angle ranges for each primary angle by watching the video
                3) Set if/else statement for what to do if a 2ndary angle goes out of range. (to be done after all primary angles are set)
                4) Edit rep count 
                '''

            ''' For reference, state the primary angles below, all others are secondary angles.
                Primary Angles: 
                                1) angle_26_a
                                2) angle_25_a
            '''

            #Use this to convert angles into percentages:
            #perc_angle = np.interp( anglename , (), (0, 100) )

            # always put the smaller angle before the larger angle, otherwise it wont work

            perc_angle26a = np.interp( angle_26_a, (62, 160), (0, 100) )
            perc_angle25a = np.interp(angle_26_a, (62, 160), (0, 100))

            #print("perc_angle25a: ", perc_angle25a, "perc_angle26a: ", perc_angle26a)
            #print(perc_angle26a)

            ''' Set if/else statements for all primary angles, use the initial-inter-final state thing if needed,
                otherwise, just write if/else statements as needed      '''
            if count < max_count:
                if   (   (angle_26_a < 168 and angle_26_a > 162) and ((angle_25_a < 168 and angle_25_a > 162)) ):
                    cv2.putText(img, "Initial State", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    rep_count_locked = 0

                elif (   (angle_26_a < 66 and angle_26_a > 58)   and (angle_25_a < 66 and angle_25_a > 58) and (rep_count_locked == 0) ):
                    cv2.putText(img, "Final State", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

                elif (  (angle_26_a > 58 and angle_26_a < 168)   and (angle_25_a > 58 and angle_25_a < 168) and (rep_count_locked == 0) ):
                    cv2.putText(img, "Intermediate State", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            ''' '''
            # SET ERROR STATES/ BOUNDARIES

            '''Section B3: Use this to count the number of repetitions + write code to 
                                send error messages if the user isn't performing them correctly'''

            ''' CREATE FUNCTION TO HANDLE THE FOLLOWING '''

            if(rep_count_locked == 0 and count < max_count):

                check_angle_error( angle_11_b, '<', 62, 0, "ERROR: Your left shoulder is bent too much")

                check_angle_error( angle_11_b, '>', 65, 1, "ERROR: Your left shoulder is too straight")

                if ( (angle_12_b < 62)):

                    if(error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[2].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your right shoulder is bent too much", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

                if ( (angle_12_b > 65)):

                    if(error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[3].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your right shoulder is too straight", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

                if ( (angle_13_a > 268)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[4].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your left elbow is getting too wide", (10, txt_w), cv2.FONT_HERSHEY_PLAIN,
                                1, (255, 0, 0), )

                if ( (angle_13_a < 240)):

                    if(error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[5].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your left elbow is bending inwards too much", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )
                    # prnt_err("ERROR: Your left elbow is bending inwards too much", txt_w)

                if ( (angle_14_a > 268)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[6].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your right elbow is getting too wide", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

                if ( (angle_14_a < 240)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[7].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your right elbow is bending inwards too much", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

                if ( (angle_23_a > 310) or (angle_24_a > 310) ):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[8].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Your shoulders & knees are too close", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

                if ( (angle_23_a < 210) or (angle_24_a < 210)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[9].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your shoulders & knees are too far away ", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), )

                if ((angle_26_a < 64) or (angle_25_a < 64)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[10].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Don't close your knees too much", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )

                if ((angle_26_a > 168) or (angle_25_a > 168)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[11].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Your knees are getting too wide", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )

            txt_w = 85
            error_already_showing = 0





            ''' I've done it the way the youtuber did, if needed, write completely different code to count the reps etc   '''

            # COUNT EXERCISE REPETITIONS:

            ''' NOTE: Apparently, sometimes, it doesnt register that the angle has reached a certain percentage value
                    use whatever values it does register by looking at the angles getting printed in the console '''

            if perc_angle26a == 100 and perc_angle25a == 100 and rep_count_locked == 0:
                if dir == 0 & passed_thru == 0:
                    count += 0.5
                    dir = 1
                    # cv2.putText(img, "Great! Move arm upwards", (10, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 210, 255), 2)

                    passed_thru = 1

                else:
                    pass

            if perc_angle26a == 0 and perc_angle25a == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0
                    passed_thru = 0
            # print(count)

            # to count full reps only, use str( int( count ) )
            if count < max_count:
                cv2.putText(img, f'Reps: {count}', (10, 52), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)



        # Exercise Monitoring ends here
            if count >= max_count:
                success_rate = 0
                for i in range(0, 10):
                    if (error_keeper[i] == 1):
                        success_rate += 10
                b1 = 110
                b2 = 82
                cv2.rectangle(img, (0, 0), (1000, 1000), (255, 255, 255), -1)
                cv2.putText(img, "EXERCISE OVER!", (b1 + 35, b2), cv2.FONT_HERSHEY_PLAIN, 2, (4, 73, 9), 2)
                cv2.putText(img, "Great Job! It looks like you're done ", (b1, b2 + 62), cv2.FONT_HERSHEY_PLAIN, 1.1,
                            (4, 73, 9), 0)
                cv2.putText(img, "with this exercise. Please take a", (b1, b2 + 82), cv2.FONT_HERSHEY_PLAIN, 1.1,
                            (4, 73, 9), 0)
                cv2.putText(img, "look at your success rate and the", (b1, b2 + 102), cv2.FONT_HERSHEY_PLAIN, 1.1,
                            (4, 73, 9), 0)
                cv2.putText(img, "error report stored on your device.", (b1, b2 + 122), cv2.FONT_HERSHEY_PLAIN, 1.1,
                            (4, 73, 9), 0)
                cv2.putText(img, f"Success Rate: {success_rate}%", (b1 + 5, b2 + 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (4, 73, 9), 2)

        #print(error_report)
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cv2.imshow("Image", img)
        if cv2.waitKey(1):
            if count == max_count:
                break

    workbook = xlsxwriter.Workbook('Exercise_Reports/Crunches_error_report.xlsx')
    worksheet = workbook.add_worksheet()

    for i in range(0, len(error_report) ):
        error_report[i][1] = len(my_set[i])

        if ( any(my_set[i]) == False):
            error_report[i][2] = "No Mistakes like this one!"
            #print(i, "#: No Mistakes!" )
        else:
            error_report[i][2] = ', '.join(my_set[i])
            #print(i, "#: ", my_set[i])
        worksheet.write(i, 0, error_report[i][0])
        worksheet.write(i, 1, error_report[i][1])
        worksheet.write(i, 2, error_report[i][2])
    workbook.close()
    print(error_report)



