from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
import cv2 as cv
import numpy as np


def load_Vmodel():
    input_tensor = Input(shape=(118, 118, 3))
    baseModel = MobileNetV2(pooling='avg',
                            include_top=False,
                            input_tensor=input_tensor, weights=None)

    headModel = baseModel.output
    headModel = Dense(1, activation="sigmoid")(headModel)

    V_model = Model(inputs=baseModel.input, outputs=headModel)
    return V_model


def predict_violence(camera_url: str) -> bool:
    model = load_Vmodel()
    model.load_weights("violence_w.h5")

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

    frame = cv.flip(frame, 1)
    pr = cv.resize(frame, (118, 118), interpolation=cv.INTER_AREA)
    pr = cv.cvtColor(pr, cv.COLOR_BGR2RGB)
    pr = np.expand_dims(pr, axis=0) / 255

    cap.release()

    probabilities = model.predict(pr)
    if probabilities > 0.5:
        return True
    else:
        return False
