import cv2 as cv
import imutils


def predict_motion(camera_url: str) -> bool:
    try:
        cap = cv.VideoCapture(camera_url)
    except:
        return False

    pframe = None
    motion = False

    for i in range(10):
        success, frame = cap.read()
        if not success:
            continue

        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        gray = cv.GaussianBlur(gray, (21, 21), 0)
        if pframe is None:
            pframe = gray
            continue
        frameDelta = cv.absdiff(pframe, gray)
        _, thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)
        dilate = cv.dilate(thresh, None, iterations=2)

        contours = cv.findContours(
            dilate.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(contours)
        for c in cnts:
            if cv.contourArea(c) < 600:
                continue
            motion = True

        pframe = gray

    cap.release()

    return motion
