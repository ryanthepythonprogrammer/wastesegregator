import cv2
import numpy as np
import tensorflow as tf

def frame_loader(frame, model):

    CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'organic']
    BINS_CATEGORIES = ['Yellow Bin/Dry Waste', 'Blue Bin/Dry Waste', 'Red Bin/Dry Waste', 'Yellow Bin/Dry Waste', 'Black Bin/Dry Waste', 'Green Bin/Wet Waste']
    new_frame = cv2.resize(frame, (224, 224))
    frame = cv2.resize(frame, (400, 400))

    features = np.array(new_frame).reshape(-1, 224,224,3)
    prediction = model.predict_classes(features)
    
    for i in prediction:
        n_prediction = CATEGORIES[i]
        bin_prediction = BINS_CATEGORIES[i]

    
    return n_prediction, bin_prediction