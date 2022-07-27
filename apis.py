from typing import Union
from fastapi import Body, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fire_detection_model2 import predict
import numpy as np

tags_metadata = [
    {"name": "Model", "description": "The AI models endpoint"},
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


class BaseResponse(BaseModel):
    predict: bool = False
    processed_frame: Union[type[np.ndarray], None] = None


@my_app.get('/', tags=['Root'])
def root():
    return {"message": "hello world!mm"}


@my_app.post('/api/Models/FireDetection', response_model=BaseResponse, tags=["Models"])
def detect_fire(frame: type[np.ndarray] = Body(description='The frame to be proccessed')):
    prediction: bool = predict(frame)

    return BaseResponse(
        predict=prediction,
        processed_frame=frame,
    )
