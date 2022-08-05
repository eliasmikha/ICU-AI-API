from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from face_recognition import predict_faces
from fire_detection_model import predict_fire
from fall_detection import predict_fall
from objects import BaseResponse, CameraRequest
from violence_detection import predict_violence
from motion_detection import predict_motion
import requests


tags_metadata = [
    {"name": "Models", "description": "The AI models endpoint"},
    {"name": "Root"}
]

description = """
ICU AI APIs will help you with your security cameras! 📷

## Models

you will be able to use:

* **Fire Detection**.
* **Fall Detection**.
* **Violence Detection**.
* **Motion Detection**.
* **Face Recognition**.
"""

my_app = FastAPI(
    title="ICU AI APIs",
    description=description,
    version="0.20.1",
    openapi_tags=tags_metadata,
)

origins = ["*"]

AUTH_URL: str = 'https://auth-icu.herokuapp.com/api/ai/newfaces'

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@my_app.get('/', tags=['Root'])
def root():
    return {"message": "hello world!"}


@my_app.post('/api/Models/Predict', tags=["Models"])
async def models_prediction(camera: CameraRequest = Body()):
    response: BaseResponse = BaseResponse(
        camid=camera.id,
    )

    response.fire = predict_fire(camera.url)

    response.fall = predict_fall(camera.url)

    response.violence = predict_violence(camera.url)

    response.motion = predict_motion(camera.url)

    response.faces = predict_faces(camera.url)

    requests.post(AUTH_URL, json=response.json())
