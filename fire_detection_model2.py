import tensorflow as tf
import numpy as np
import cv2 as cv

def predict(camera_url: str):
   cap = cv.VideoCapture(camera_url)
   frame: np.ndarray

   for i in range(len(10)):
      success, frame = cap.read()
      if not success:
         return False

   frame = cv.flip(frame, 1)
   pr = cv.resize(frame, (112, 112), interpolation=cv.INTER_AREA)
   pr = cv.cvtColor(pr, cv.COLOR_BGR2RGB)
   pr = pr.astype(np.float32)
   pr = np.expand_dims(pr, axis=0) / 255
   # Load the TFLite model and allocate tensors.
   interpreter = tf.lite.Interpreter(model_path='converted_model.tflite')
   interpreter.allocate_tensors()
   # Get input and output tensors.
   input_details = interpreter.get_input_details()
   output_details = interpreter.get_output_details()
   # Set up your input data.
   # Invoke the model on the input data
   interpreter.set_tensor(input_details[0]['index'], pr)
   interpreter.invoke()
   # Get the result 
   output_data = interpreter.get_tensor(output_details[0]['index'])
   if output_data >= 0.6:
      return True
   return False
