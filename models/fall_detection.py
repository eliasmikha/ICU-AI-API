import cv2 as cv
import mediapipe as mp
import numpy as np


def predict_fall(camera_url: str) -> bool:
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    pose = mpPose.Pose()
    try:
        cap = cv.VideoCapture(camera_url)
    except:
        return False
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    frame: np.ndarray = None

    for i in range(10):
        success, frame = cap.read()
        if success is False:
            continue

    if frame is None:
        return False

    cap.release()

    frame = cv.resize(frame, (640, 480), interpolation=cv.INTER_AREA)
    frame = cv.flip(frame, 1)
    rgbFrame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = pose.process(rgbFrame)
    # print(result.pose_landmarks
    landmarks = result.pose_landmarks
    h, w, c = frame.shape
    yList = []
    xList = []
    if landmarks:
        mpDraw.draw_landmarks(frame, landmarks, mpPose.POSE_CONNECTIONS)
        for id, ln in enumerate(result.pose_landmarks.landmark):
            yList.append(ln.y)
            xList.append(ln.x)
        min_y, max_y = min(yList),  max(yList)
        min_x, max_x = min(xList), max(xList)
        if abs(max_y - min_y) > 2 * abs(max_x - min_x):
            return False
        return True
    return False
