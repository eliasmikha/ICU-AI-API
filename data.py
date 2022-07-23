from typing import Union
from base_model import CameraResponse


id_increment: int = 1
cameras: dict[int, CameraResponse] = {}


def increment_id():
    global id_increment
    id_increment += 1

def get_camera(id: int) -> Union[CameraResponse, None]:
    global cameras
    for i in cameras.keys():
        if i == id:
            return cameras[i]
    
    return None
