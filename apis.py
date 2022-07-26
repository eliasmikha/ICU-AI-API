from typing import Union
from fastapi import Body, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fire_detection_model import predict_fire
import numpy as np

app = FastAPI()

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


@app.post('/api/Models/FireDetection', response_model=BaseResponse)
async def detect_fire(frame: np.ndarray = Body('The frame to be proccessed')):
    prediction: bool = predict_fire(frame)

    return BaseResponse(
        predict=prediction,
        processed_frame=frame,
    )
