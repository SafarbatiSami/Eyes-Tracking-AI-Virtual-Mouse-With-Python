import cv2
import mediapipe as mp
import pyautogui


cam = cv2.VideoCapture(0) #open the webcam
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size() # To get the screen size


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1) # to invert the webcam in y axis
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    #print(landmark_points)
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]): #for all the landmarks detected in the right eye
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0)) #draw the green circles in the eye
            if id==1:
                screen_x = screen_w / frame_w * (x*1.4) #to get the ratio
                screen_y = screen_h / frame_h * (y*1.4)
                pyautogui.moveTo(screen_x, screen_y) # to move the cursor
        left = [landmarks[145], landmarks[159]]
        for landmark in left:  #for all landmarks detected in the left eyes
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0,255,255)) # draw the yellow circles
        if abs(left[0].y - left[1].y) < 0.005: #test if the the two yellow landmarks are close
            print('click')
            pyautogui.click() #to click
            pyautogui.sleep(1)


    cv2.imshow('Eyes Mouse AI', frame)
    cv2.waitKey(1)