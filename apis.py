from typing import Union
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fire_detection_model2 import predict

tags_metadata = [
    {"name": "Models", "description": "The AI models endpoint"},
    {"name": "Root"}
]

description = """
ICU AI APIs will help you with your security cameras! 📷

## Models

you will be able to use:

* **Fire Detection**.
* **Motion Detection** (_not implemented yet_).
* **Fall Detection** (_not implemented yet_).
* **Face Recognition** (_not implemented yet_).
* **Violence Detection** (_not implemented yet_).
"""

my_app = FastAPI(
    title="ICU AI APIs",
    description=description,
    version="0.17.3",
    openapi_tags=tags_metadata,
    )

origins = ["*"]

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BaseOptions(BaseModel):
    fire: Union[bool, None] = False
    face: Union[bool, None] = False
    fall: Union[bool, None] = False
    motion: Union[bool, None] = False
    violence: Union[bool, None] = False


class BaseResponse(BaseModel):
    cameraId: Union[int, None] = None
    predictions: BaseOptions


class CameraRequest(BaseModel):
    id: Union[int, None] = None
    url: str
    options: BaseOptions


@my_app.get('/', tags=['Root'])
def root():
    return {"message": "hello world!"}


@my_app.post('/api/Models/Predict', response_model=BaseResponse, tags=["Models"])
async def models_prediction(camera: CameraRequest = Body()):
    response: BaseResponse = BaseResponse(
        predictions=BaseOptions(),
        cameraId=camera.id
    )

    if camera.options.fire:
        prediction: bool = predict(camera.url)
        response.predictions.fire = prediction

    return response
