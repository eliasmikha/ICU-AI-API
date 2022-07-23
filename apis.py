from typing import Union
from datetime import datetime
from fastapi import Body, FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from data import *
from base_model import CameraModel, CameraResponse, SuccessResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {"message": "hello world!"}


@app.post('/api/Admin/AddCamera', response_model=SuccessResponse)
def add_camera(
    camera: CameraModel = Body(description='A camera object to be added')
):
    global cameras
    cameras[id_increment] = CameraResponse(
        id=id_increment,
        creationDate=datetime.now(),
        result={
            "camera": camera
        },
        success=True
    )
    increment_id()
    return SuccessResponse(
        message='camera added successfully',
        success=True
    )


@app.get('/api/Admin/Camera/Details', response_model=SuccessResponse)
def get_camera_details(
    id: int = Query(description='')
):
    camera: Union[CameraResponse, None] = get_camera(id)
    print(camera)
    if camera == None:
        return SuccessResponse(
            error='Camera not found, check the id and try again',
            success=False
        ),
    else:
        return SuccessResponse(
            result=camera,
            success=True
        ),
