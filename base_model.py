from datetime import datetime
from pydantic import BaseModel
from typing import Union, Any

class BaseResponse(BaseModel):
    message: Union[str, None] = None
    error: Union[str, None] = None
    success: bool = True

class SuccessResponse(BaseResponse):
    result: Union[dict[str, Any], None] = None

class BaseResponseClass(BaseModel):
    id: int
    creationDate: datetime

class CameraModel(BaseModel):
    url: str
    isActive: bool

class CameraResponse(BaseResponseClass):
    result: dict[str, CameraModel]
