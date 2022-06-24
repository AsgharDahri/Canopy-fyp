import cv2
import numpy as np
import time
import PoseModule as pm
import xlsxwriter
import math

# IF IT CAN'T RECOGNISE THESE LIBRARIES, GO TO PYTHON INTERPRETER -> AVAILABLE PACKAGES - > install the relevant package
txt_w = 85
error_already_showing = 0
# TO RUN A FILE FOR THE FIRST TIME, IN THE TOP-RIGHT CORNER, RUN -> "Run..." -> SELECT FILE NAME (Crunches_Tracker.py)
def bHips():
        
    print("Bridging_Hips.py")
    """  REGARDING SUCCESS RATE, UPDATE THE ERROR_KEEPER'S RESPC. VALUE FOR EACH ERROR """

    # "Resources/man_performing_bicep_curls_micro.mp4"
    cap = cv2.VideoCapture("Resources/bridging_hips.mp4")

    detector = pm.PoseDetector()
    error_keeper = [1 for i in range(10)]
    max_count = 2
    count = 0
    rep_count_locked = 1

    # 0 = going up, 1 = going down
    dir = 0

    ''' In the following code, we've defined a 3D array used to store the error report and its details 
        along with a set called my_set that is used to store the reps in which those specific errors were made'''

    arr = np.array(['0' for i in range(18)], dtype=object)

    error_report = arr.reshape(6, 3)

    my_set = [set() for _ in range(6)]

    for i in range(0, len(error_report)):
        error_report[i][1] = 0

    ''' Here, we've defined the error messages for key-points # 11 to 28 [See Pose Landmarks Diagram] 
        you can edit the messages if needed.
        
    Your left shoulder isn't aligned with your left foot
    Your right shoulder isn't aligned with your right foot
    Your left heel is above the ground
    Your left heel is bent inwards too much
    Your right heel is above the ground
    Your right heel is bent inwards too much
        
    '''

    error_report[0][0] = 'Your left shoulder isn\'t aligned with your left foot'
    error_report[1][0] = 'Your right shoulder isn\'t aligned with your right foot'
    error_report[2][0] = 'Your left heel is above the ground'
    error_report[3][0] = 'Your left heel is bent inwards too much'
    error_report[4][0] = 'Your right heel is above the ground'
    error_report[5][0] = 'Your right heel is bent inwards too much'


    ''' The following function is used to picka particular angle, and set a condition in order to 
        define an error message if the condition is met -- USE IS OPTIONAL'''

    # These are used to make sure that multiple error messages do not overlap:
   


    def check_angle_error(angle_name, sign, angle_val, my_set_val, message):
        global txt_w, error_already_showing
        if (sign == '<'):
            # print("beep")
            if ((angle_name < angle_val)):

                if (error_already_showing == 1):
                    txt_w = txt_w + 15

                error_already_showing = 1

                my_set[my_set_val].add(str(round(count)))
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


    while True:
        success, img = cap.read()

        passed_thru = 0
        # Comment this out when you use the webcam

        # img = cv2.resize( img, (480, 710)) # This is used to resize the video/webcam footage

        # Exercise Monitoring begins here

        # This is used to find all the landmarks in the video
        img = detector.findPose(img,
                                False)  # Set the 2nd param to true if you want to see every single landmark + connection

        # Section A1 starts here: The following code is being used to find the landmarks that we're going to use
        # your landmarks are prob. diff. from the youtuber's...

        # lmList is used to segment the list into individual frames and store them frame-by-frame in an array
        lmList = detector.findPosition(img, False)  # Set the 2nd param to true if you want to see every single landmark

        # print("\nPoint: ", lmList)

        if len(lmList) != 0:
            cv2.rectangle(img, (0, 0), (210, 70), (255, 255, 255), -1)
            ''' Section B1: This is where most of the work is done, 90% of all additions/changes will occur here: '''
            #   This is what we're going to do:
            #   1) we're going to calculate the angle at each landmark w.r.t  to all of its adjacent landmarks,
            #   2) then use if-else statements to set initial, final positions etc after identifying primary angles
            #   3) then set conditions on secondary angles to make sure the user performs them correctly

            #  Params: SRC, Point1, Center Point/Point2, Point3, Show Angle or not?
            # angle = detector.findAngle(img, 11, 13, 15, 1)

            # Use the following angles, if needed, create a new one or change landmarks:
            # Angle naming convention: angle_centrepoint_subcat

            angle_11_a = detector.findAngle(img, 12, 11, 31, 0)
            # angle_11_b = detector.findAngle(img, 13, 11, 23, 1)

            angle_12_a = detector.findAngle(img, 11, 12, 32, 0)
            # angle_12_b = detector.findAngle(img, 14, 12, 24, 1)

            # angle_13_a = detector.findAngle(img, 11, 13, 15, 0)

            # angle_14_a = detector.findAngle(img, 12, 14, 16, 1)

            # angle_15_a = detector.findAngle(img, 13, 15, 19, 1)
            # angle_15_b = detector.findAngle(img, 13, 15, 17, 1)

            # angle_16_a = detector.findAngle(img, 14, 16, 20, 1)
            # angle_16_b = detector.findAngle(img, 14, 16, 18, 1)

            angle_23_a = detector.findAngle(img, 11, 23, 25, 0)

            angle_24_a = detector.findAngle(img, 12, 24, 26, 0)

            # angle_25_a = detector.findAngle(img, 23, 25, 27, 1)

            # angle_26_a = detector.findAngle(img, 24, 26, 28, 1)

            # angle_27_a = detector.findAngle(img, 25, 27, 31, 1)
            # angle_27_b = detector.findAngle(img, 25, 27, 29, 1)

            # angle_28_a = detector.findAngle(img, 26, 28, 32, 1)
            # angle_28_b = detector.findAngle(img, 26, 28, 30, 1)

            angle_29_b = detector.findAngle(img, 11, 29, 31, 0)
            angle_30_b = detector.findAngle(img, 12, 30, 32, 1)

            ''' Section B2: Do the following:
                1) Calculate/convert the primary angles into percentage values.
                2) Find & set the app. initial/final/inter angle ranges for each primary angle by watching the video
                3) Set if/else statement for what to do if a 2ndary angle goes out of range. (to be done after all primary angles are set)
                4) Edit rep count 
                '''

            ''' For reference, state the primary angles below, all others are secondary angles.
                Primary Angles: 
                                1) angle_23_a
                                2) angle_24_a
            '''

            # Use this to convert angles into percentages:
            # always put the smaller angle before the larger angle, otherwise it wont work

            # perc_angle = np.interp( angle_name , (), (0, 100) )
            # print(perc_angle)

            ''' Set if/else statements for all primary angles, use the initial-inter-final state thing if needed,
                otherwise, just write if/else statements as needed   '''


                                    # Add/Remove 'and' based on the number of primary angles
            if count < max_count:
                if   (   (angle_23_a < 188 and angle_23_a > 168) and (angle_24_a < 192 and angle_24_a > 172) ):
                    cv2.putText(img, "Final State", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    if rep_count_locked == 0:
                        if dir == 0 & passed_thru == 0:
                            count += 0.5
                            dir = 1
                            # cv2.putText(img, "Great! Move arm upwards", (10, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 210, 255), 2)

                            passed_thru = 1

                    else:
                        pass

                elif (   (angle_23_a < 130 and angle_23_a > 120)   and (angle_24_a < 130 and angle_24_a > 120)  ):
                    cv2.putText(img, "Initial State", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    rep_count_locked = 0
                    if dir == 1:
                        count += 0.5
                        dir = 0
                        passed_thru = 0

                elif (  (angle_23_a > 123 and angle_23_a < 123)   and (angle_24_a > 58 and angle_24_a < 168)  ):
                    cv2.putText(img, "Intermediate State", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

                cv2.putText(img, f'Reps: {count}', (10, 52), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)


            '''Section B3: Use this to count the number of repetitions + write code to 
                                send error messages if the user isn't performing them correctly'''

            ''' You've got 2 options:
                1) Use the function called check_angle_error( angle_name, sign, angle_val, my_set_val, message ):
                HOW: simply fill up the params and test 'em, pay attention to txt_w & error_already_showing 

                2) Directly edit if/else statements, in which case, change the following: 
                angle_name, sign, angle_val, my_set_val (This is the index position for the my_set[i] array), message
                '''


            if (rep_count_locked == 0 and count < max_count):

                #check_angle_error(angle_11_b, '<', 62, 0, "ERROR: Your left shoulder is bent too much")

                #check_angle_error(angle_11_b, '>', 65, 1, "ERROR: Your left shoulder is too straight")

                if ((angle_11_a < 72) or (angle_11_a > 89)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[0].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your left shoulder isn't aligned with your left foot", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )

                if ((angle_12_a < 250) or (angle_12_a > 266)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[1].add(str(round(count)))
                    error_keeper[round(count)] = 0
                    cv2.putText(img, "ERROR: Your right shoulder isn't aligned with your right foot", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )

                if ((angle_29_b > 185)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[2].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Your left heel is above the ground", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )


                if ((angle_29_b < 175)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[3].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Your left heel is bent inwards too much", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )

                if ((angle_30_b > 180)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[4].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Your right heel is above the ground", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )


                if ((angle_30_b < 168)):

                    if (error_already_showing == 1):
                        txt_w = txt_w + 15
                    error_already_showing = 1
                    my_set[5].add(str(round(count)))
                    error_keeper[round(count)] = 0

                    cv2.putText(img, "ERROR: Your right heel is bent inwards too much", (10, txt_w), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), )


            txt_w = 85
            error_already_showing = 0


            ''' I've done it the way the youtuber did, if needed, write completely different code to count the reps etc   '''

            # COUNT EXERCISE REPETITIONS:

            ''' NOTE: Apparently, sometimes, it doesnt register that the angle has reached a certain percentage value
                    use whatever values it does register by looking at the angles getting printed in the console '''
            '''
            if perc_angle == 100 and rep_count_locked == 0:
                if dir == 0 & passed_thru == 0:
                    count += 0.5
                    dir = 1
                    # cv2.putText(img, "Great! Move arm upwards", (10, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 210, 255), 2)

                    passed_thru = 1

                else:
                    pass

            if perc_angle == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0
                    passed_thru = 0
            # print(count)

            # to count full reps only, use str( int( count ) )

            cv2.putText(img, f'Reps: {count}', (10, 52), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            '''

            ''' NOTE: Once the app gets integrated, watch the video again and:
                    1) incorporate time into the exercises to improve monitoring quality.
                    2) Style the landmarks/connections. '''

        # Exercise Monitoring ends here
            if count >= max_count:
                success_rate = 0
                for i in range(0, 10):
                    if (error_keeper[i] == 1):
                        success_rate += 10
                b1 = 130
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
                cv2.putText(img, f"Success Rate: {success_rate}%", (b1 + 5, b2 + 220), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (4, 73, 9), 2)
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cv2.imshow("Image", img)
        if cv2.waitKey(1):
            if count == max_count:
                break

    ''' In the following section, we write the error report onto an excel file'''

    workbook = xlsxwriter.Workbook('Exercise_Reports/Bridges_error_report.xlsx')  # Change file name acc. to exercise
    worksheet = workbook.add_worksheet()

    for i in range(0, len(error_report)):
        error_report[i][1] = len(my_set[i])

        if (any(my_set[i]) == False):
            error_report[i][2] = "No Mistakes like this one!"
            # print(i, "#: No Mistakes!" )
        else:
            error_report[i][2] = ', '.join(my_set[i])
            # print(i, "#: ", my_set[i])
        worksheet.write(i, 0, error_report[i][0])
        worksheet.write(i, 1, error_report[i][1])
        worksheet.write(i, 2, error_report[i][2])
    workbook.close()
    print(error_report)


