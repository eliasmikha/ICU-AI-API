from typing import Union
from numpy import double
from pydantic import BaseModel


# class BaseOptions(BaseModel):
#     fire: Union[bool, None] = False
#     face: Union[bool, None] = False
#     fall: Union[bool, None] = False
#     motion: Union[bool, None] = False
#     violence: Union[bool, None] = False


class BaseResponse(BaseModel):
    camid: Union[int, None] = None
    fire: bool = False
    fall: bool = False
    motion: bool = False
    violence: bool = False
    faces: list[list] = []


class CameraRequest(BaseModel):
    id: Union[str, None] = None
    url: Union[str, None] = None
    name: Union[str, None] = None


class BaseError(BaseModel):
    success: bool = False
    message: str
