import cv2 as cv
import numpy as np
import module as m
import time
import cv2
from deepface import DeepFace
import numpy as np
import json
# Load the pre-trained emotion detection model
model = DeepFace.build_model("Emotion")
# Define emotion labels
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
# Define emotion colors
emotion_count = {
    'angry': 0,
    'disgust': 0,
    'fear': 0,
    'happy': 0,
    'sad': 0,
    'surprise': 0,
    'neutral': 0
}
# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variables
COUNTER = 0
TOTAL_BLINKS = 0
CLOSED_EYES_FRAME = 3
cameraID = 0
videoPath = "Video/Your Eyes Independently_Trim5.mp4"
# variables for frame rate.
FRAME_COUNTER = 0
START_TIME = time.time()
FPS = 0
deviation_count = 0

# creating camera object
camera = cv.VideoCapture(0)
camera.set(3, 300)
camera.set(4, 170)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
f = camera.get(cv.CAP_PROP_FPS)
width = 300
height = 200
print(width, height, f)
fileName = videoPath.split('/')[1]
name = fileName.split('.')[0]
print(name)


while True:
    FRAME_COUNTER += 1
    # getting frame from camera
    ret, frame = camera.read()
    if ret == False:
        break

    # converting frame into Gry image.
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayFrame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = grayFrame[y:y + h, x:x + w]

        # Resize the face ROI to match the input shape of the model
        resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)

        # Convert the resized face to a 3-channel image
        resized_face_color = cv2.cvtColor(resized_face, cv2.COLOR_GRAY2BGR)

        # Normalize the resized face image
        normalized_face = resized_face_color.astype(np.float32) / 255.0

        # Reshape the image to match the input shape of the model
        reshaped_face = normalized_face.reshape(1, 48, 48, 3)

        # Predict emotions using the pre-trained model
        preds = model.predict(reshaped_face)
        emotion_idx = preds.argmax()
        emotion = emotion_labels[emotion_idx]

        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        emotion_count[emotion] += 1
        print(emotion, emotion_count[emotion])

    height, width = grayFrame.shape
    circleCenter = (int(width/2), 50)
    # calling the face detector funciton
    image, face = m.faceDetector(frame, grayFrame)
    if face is not None:

        # calling landmarks detector funciton.
        image, PointList = m.faceLandmakDetector(frame, grayFrame, face, False)
        # print(PointList)

        cv.putText(frame, f'FPS: {round(FPS,1)}',
                   (460, 20), m.fonts, 0.7, m.YELLOW, 2)
        RightEyePoint = PointList[36:42]
        LeftEyePoint = PointList[42:48]
        leftRatio, topMid, bottomMid = m.blinkDetector(LeftEyePoint)
        rightRatio, rTop, rBottom = m.blinkDetector(RightEyePoint)
        # cv.circle(image, topMid, 2, m.YELLOW, -1)
        # cv.circle(image, bottomMid, 2, m.YELLOW, -1)

        blinkRatio = (leftRatio + rightRatio)/2
        cv.circle(image, circleCenter, (int(blinkRatio*4.3)), m.CHOCOLATE, -1)
        cv.circle(image, circleCenter, (int(blinkRatio*3.2)), m.CYAN, 2)
        cv.circle(image, circleCenter, (int(blinkRatio*2)), m.GREEN, 3)

        if blinkRatio > 2:
            COUNTER += 1
            cv.putText(image, f'Blink', (70, 50),
                       m.fonts, 0.8, m.LIGHT_BLUE, 2)
            # print("blink")
        else:
            if COUNTER > CLOSED_EYES_FRAME:
                TOTAL_BLINKS += 1
                COUNTER = 0
        cv.putText(image, f'Total Blinks: {TOTAL_BLINKS}', (230, 17),
                   m.fonts, 0.5, m.ORANGE, 2)

        # for p in LeftEyePoint:
        #     cv.circle(image, p, 3, m.MAGENTA, 1)
        mask, pos, color = m.EyeTracking(frame, grayFrame, RightEyePoint)
        maskleft, leftPos, leftColor = m.EyeTracking(
            frame, grayFrame, LeftEyePoint)

        # draw background as line where we put text.
        cv.line(image, (30, 90), (100, 90), color[0], 30)
        cv.line(image, (25, 50), (135, 50), m.WHITE, 30)
        cv.line(image, (int(width-150), 50), (int(width-45), 50), m.WHITE, 30)
        cv.line(image, (int(width-140), 90),
                (int(width-60), 90), leftColor[0], 30)

        # writing text on above line
        cv.putText(image, f'{pos}', (35, 95), m.fonts, 0.6, color[1], 2)
        cv.putText(image, f'{leftPos}', (int(width-140), 95),
                   m.fonts, 0.6, leftColor[1], 2)
        cv.putText(image, f'Right Eye', (35, 55), m.fonts, 0.6, color[1], 2)
        cv.putText(image, f'Left Eye', (int(width-145), 55),
                   m.fonts, 0.6, leftColor[1], 2)
        if pos == 'Left' or pos == 'Right':
           deviation_count += 1

        print(pos, " ", deviation_count)
        # showing the frame on the screen
        cv.imshow('Frame', image)
    else:
        cv.imshow('Frame', frame)

    # Recoder.write(frame)
    # calculating the seconds
    SECONDS = time.time() - START_TIME
    # calculating the frame rate
    FPS = FRAME_COUNTER/SECONDS
    # print(FPS)
    # defining the key to Quite the Loop

    key = cv.waitKey(1)

    # if q is pressed on keyboard: quit
    if key == ord('q'):
        current_date = time.strftime("%Y-%m-%d")
        data = {
            'date': current_date,
            'deviation_count': deviation_count,
            'emotion_count': emotion_count
        }
        print(data)
        with open('data.json', 'w') as f:
            json.dump(data, f)
        break
# closing the camera
camera.release()
# Recoder.release()
# closing  all the windows
cv.destroyAllWindows()
