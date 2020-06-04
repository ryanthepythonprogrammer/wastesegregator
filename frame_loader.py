import cv2
import numpy as np
import keras
import tensorflow


def frame_loader():
    cap = cv2.VideoCapture(1)
    while True:
        _,frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        new_frame = cv2.resize(frame, (224, 224))
        frame = cv2.resize(frame, ())
        CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        model = keras.models.load_model("models/new_ft.model")
        features = np.array(new_frame).reshape(-1, 224,224,3)
        prediction = model.predict([features])
        for i in range(0,5):
            if int(prediction) == i:
                cv2.putText(frame, (CATEGORIES[i]), (205, 250), cv2.FONT_HERSHEY_COMPLEX,0.7,(255, 255, 0))
    
        #cv2.imshow('frame', frame)

        if cv2.waitKey(1) == 27: 
            break

        return frame, int(prediction)

    cap.release()
    cv2.destroyAllWindows()