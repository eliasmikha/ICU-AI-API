from typing import Union
from fastapi import Body, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fire_detection_model2 import predict
import numpy as np

my_app = FastAPI()

origins = ["*"]

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BaseResponse(BaseModel):
    predict: bool = False
    processed_frame: Union[type[np.ndarray], None] = None


@my_app.get('/', tags=['Root'])
def root():
    return {"message": "hello world!"}


@my_app.post('/api/Models/FireDetection', response_model=BaseResponse, tags=["Models"])
def detect_fire(frame: type[np.ndarray] = Body(description='The frame to be proccessed')):
    prediction: bool = predict(frame)

    return BaseResponse(
        predict=prediction,
        processed_frame=frame,
    )
