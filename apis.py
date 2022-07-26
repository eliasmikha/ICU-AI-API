from typing import Union
from fastapi import Body, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fire_detection_model2 import predict
import numpy as np

tags_metadata = [
    {"name": "Models", "description": "AI Models endpoints"}
]

app = FastAPI(openapi_tags=tags_metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BaseResponse(BaseModel):
    predict: bool = False
    processed_frame: Union[np.ndarray, None] = None


@app.get('/')
def root():
    return {"message": "hello world!"}


@app.post('/api/Models/FireDetection', response_model=BaseResponse, tags=["Models"])
async def detect_fire(frame: np.ndarray = Body('The frame to be proccessed')):
    prediction: bool = predict(frame)

    return BaseResponse(
        predict=prediction,
        processed_frame=frame,
    )
