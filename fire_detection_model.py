from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input, Dropout
import cv2 as cv
import numpy as np


def fire_model() -> Model:
    input_tensor = Input(shape=(112, 112, 3))

    base_model = InceptionV3(input_tensor=input_tensor, include_top=False)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.25)(x)
    x = Dense(8, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    return model


def predict_fire(model: Model, camera_url: str) -> bool:
    try:
        cap = cv.VideoCapture(camera_url)
    except:
        return False

    frame: np.ndarray = None

    for i in range(5):
        success, frame = cap.read()
        if not success:
            continue

    if frame is None:
        return False

    cap.release()

    frame = cv.flip(frame, 1)
    pr = cv.resize(frame, (112, 112), interpolation=cv.INTER_AREA)
    pr = cv.cvtColor(pr, cv.COLOR_BGR2RGB)
    pr = np.expand_dims(pr, axis=0) / 255
    probabilities = model.predict(pr)

    if probabilities >= 0.6:
        return True
    return False
