
# Questo progetto utilizza Google Mediapipe, che è rilasciato sotto licenza Apache 2.0.
# Licenza completa: https://www.apache.org/licenses/LICENSE-2.0



from typing import Tuple, Union
import math
import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import time 

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def _normalized_to_pixel_coordinates(
    xValues : float, yValues : float , ImgWidth : int , ImgHZeight : int):

    def AreNormalized(Value: float):
        return(Value > 0 or math.isclose(0,Value) ) and (Value <1 or math.isclose(1,Value))

    if not (AreNormalized(xValues) and AreNormalized(yValues)):
        print("Values are not normalized")
        return None
    xCord = min(math.floor(xValues * ImgWidth),ImgWidth - 1 )
    yCord = min(math.floor(yValues * ImgHZeight), ImgHZeight - 1 )

    return xCord , yCord



def Visualize(image,detetion_Result):

    annotated_img = image.copy()

    alt, lung , _ = image.shape


    for detection in detetion_Result.detections:
        bbox = detection.bounding_box
        start_point = bbox.origin_x , bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(annotated_img, start_point, end_point, TEXT_COLOR, 3)
    

        for keypoint in detection.keypoints:
            keypointpx = _normalized_to_pixel_coordinates(keypoint.x,keypoint.y,lung,alt)
            color = (0, 255, 0)
            cv2.circle(annotated_img, keypointpx, 2, color, 2)

        category = detection.categories[0]
        categoryname = category.category_name
        categoryname = '' if categoryname is None else categoryname
        probability = round(category.score, 2)
        result_text = categoryname + ' (' + str(probability) + ')'
        text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(annotated_img, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)
    
    return annotated_img


def IniziaLoShow():
    base_options = python.BaseOptions(model_asset_path='detector.tflite')
    options = vision.FaceDetectorOptions(base_options=base_options,running_mode=vision.RunningMode.VIDEO)
    detector = vision.FaceDetector.create_from_options(options)

    webcam = cv2.VideoCapture(0)

    while True:
        ret, frame = webcam.read()
        if not ret:
            break
        
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=framergb
    )

        timestamp_ms = int(time.time() * 1000)
        detection_result = detector.detect_for_video(mp_image,timestamp_ms)

        annotated_image = Visualize(frame, detection_result)
        cv2.imshow("Result", annotated_image)
        
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
                
        

    

    
    
IniziaLoShow()