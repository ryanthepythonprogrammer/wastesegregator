# SegreCAM - The Waste Segregator by Ryan Punamiya
This is a program that can segregate waster using Keras, Tensorflow, OpenCV for the neural networks and Tkinter for the GUI

## Downloads and References
This project is trained on a waste classificaation kaggle dataset which is on this repo as data.zip

## How to train 
1. Download data.zip and model.zip (ignore if cloning/downloading this repo)
2. Run on cmd: 
    `pip install -r requirements.txt`
3. Place the data zip file into the same repo as the train.py file (ignore if cloning/downloading the repo)
4. Go into the directory train.py is located in and run train.py on cmd using:
    `python train.py`

## How to run GUI 
1. Place the models folder, assets and proj_backend.py into the same repo as the main.py file (ignore if cloning the repo)
2. In the same directory, run train.py on cmd using:
    `python main.py`
    
## Important Notes 
- The default video input is set to the default webcam. In case you want to change the source, open main.py and go to line 41:
    `cap = cv2.VideoCapture(0)`
    and change the '0' to '1' for the next input and so on.
- The program will take time to open the segregator as it imports the model everytime you run the program
- The model uses ImageNet as the neural network for training. If you want to add more images to the training dataset, resize images to 224,   224.
