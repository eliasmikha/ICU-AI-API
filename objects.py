from typing import Union
from pydantic import BaseModel


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


class BaseError(BaseModel):
    success: bool = False
    message: str
