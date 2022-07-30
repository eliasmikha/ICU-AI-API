from ctypes import Union
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fire_detection_model2 import predict

tags_metadata = [
    {"name": "Models", "description": "The AI models endpoint"},
    {"name": "Root"}
]

my_app = FastAPI(openapi_tags=tags_metadata)

origins = ["*"]

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BaseOptions(BaseModel):
    fire: bool = False
    face: bool = False
    fall: bool = False
    motion: bool = False
    violence: bool = False


class BaseResponse(BaseModel):
    predictions: BaseOptions
    id: Union[int, None] = None


class CameraRequest(BaseModel):
    id: Union[int, None] = None
    url: str
    options: BaseOptions


@my_app.get('/', tags=['Root'])
def root():
    return {"message": "hello world!"}


@my_app.post('/api/Models/Predict', response_model=BaseResponse, tags=["Models"])
def detect_fire(camera: CameraRequest = Body()):
    response: BaseResponse = BaseResponse()
    response.id = camera.id

    if camera.options.fire:
        prediction: bool = predict(camera.url)
        response.predictions.fire = prediction

    return response
