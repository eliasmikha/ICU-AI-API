from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fire_detection_model2 import predict_fire
from fall_detection import predict_fall
from objects import BaseOptions, BaseResponse, CameraRequest
from violence_detection import predict_violence

tags_metadata = [
    {"name": "Models", "description": "The AI models endpoint"},
    {"name": "Root"}
]

description = """
ICU AI APIs will help you with your security cameras! 📷

## Models

you will be able to use:

* **Fire Detection**.
* **Fall Detection**.
* **Violence Detection**.
* **Motion Detection** (_not implemented yet_).
* **Face Recognition** (_not implemented yet_).
"""

my_app = FastAPI(
    title="ICU AI APIs",
    description=description,
    version="0.18.0",
    openapi_tags=tags_metadata,
)

origins = ["*"]

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@my_app.get('/', tags=['Root'])
def root():
    return {"message": "hello world!"}


@my_app.post('/api/Models/Predict', response_model=BaseResponse, tags=["Models"])
async def models_prediction(camera: CameraRequest = Body()):
    response: BaseResponse = BaseResponse(
        predictions=BaseOptions(),
        cameraId=camera.id
    )

    # if camera.options.fire:
    #     prediction: bool = predict_fire(camera.url)
    #     response.predictions.fire = prediction

    if camera.options.fall:
        prediction: bool = predict_fall(camera.url)
        response.predictions.fall = prediction
    
    if camera.options.violence:
        prediction: bool = predict_violence(camera.url)
        response.predictions.violence = prediction

    return response
