import face_recognition as fg
import cv2 as cv

def predict_faces(camera_url: str) -> list:
    try:
        cap = cv.VideoCapture(camera_url)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    except:
        return []

    frame = None

    for i in range(5):
        success, frame = cap.read()
        if not success:
            continue

    if frame is None:
        return []

    encoding_S = fg.face_encodings(frame)
    try:
        locat = fg.face_locations(frame)
        return encoding_S
    except IndexError:
        return []
