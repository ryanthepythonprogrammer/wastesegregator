# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RU9dkC9_xN-qcBpfOcOQi7xeVYMrUUI-
"""

from zipfile import ZipFile

with ZipFile('data.zip', 'r') as zipObj:
  zipObj.extractall()

with ZipFile('models.zip', 'r') as zipObj:
  zipObj.extractall()

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, cohen_kappa_score, roc_auc_score, roc_curve
from collections import Counter
from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split

from keras.applications.mobilenet import preprocess_input, MobileNet
from keras.models import Model, load_model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.preprocessing import image
from keras.optimizers import SGD
from keras.models import Sequential


IM_WIDTH, IM_HEIGHT = 224, 224
NB_EPOCHS = 1
BAT_SIZE = 32


# def get_images(paths):
#     images = []
#     for path in paths:
#         img = image.load_img(path, target_size=(224, 224))
#         x = image.img_to_array(img)
#         #x = np.expand_dims(x, axis=0)
#         x = preprocess_input(x)
#         images.append(x)

#     return np.asarray(images)


# def one_hot_encoding(labels):
#     labels = pd.Series(labels).str.get_dummies()

#     return labels


# def split(files):
#     X_train, X_test = train_test_split(files, test_size=0.20, random_state=42)
#     X_train, X_valid = train_test_split(
#         X_train, test_size=0.10, random_state=42)

#     return X_train, X_test, X_valid


# def get_labels(data_paths):
#     labels = []
#     for path in data_paths:
#         labels.append(os.path.basename(os.path.dirname(path)))

#     print(labels)

#     return labels


def fine_tune(model):

    for layer in model.layers[:95]:
        layer.trainable = False
    for layer in model.layers[95:]:
        layer.trainable = True

    model.compile(
        optimizer=SGD(lr=0.0001, momentum=0.9),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])


# def get_data_paths():

#     data_folders = glob.glob(os.path.join('data', '*'))

#     train_paths = []
#     test_paths = []
#     valid_paths = []

#     for folder in data_folders:
#         files = glob.glob(os.path.join(folder, '*.jpg'))
#         train, test, valid = split(files)

#         train_paths = train_paths + train
#         test_paths = test_paths + test
#         valid_paths = valid_paths + valid

#     np.random.shuffle(train_paths)
#     np.random.shuffle(test_paths)
#     np.random.shuffle(valid_paths)

#     print(np.asarray(train_paths), np.asarray(test_paths), np.asarray(
#         valid_paths))
#     return np.asarray(train_paths), np.asarray(test_paths), np.asarray(
#         valid_paths)



CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
DATADIR = 'data/train'

from tqdm import tqdm
import os
import cv2

IMG_SIZE = 224


training_data = []

def create_training_data():
    for category in CATEGORIES: 

        path = os.path.join(DATADIR, category) 
        class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=dog 1=cat

        for img in tqdm(os.listdir(path)):  
              img_array = cv2.imread(os.path.join(path,img)) 
              new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
              training_data.append([new_array, class_num])  # add this to our training_data

            #except OSError as e:
            #    print("OSErrroBad img most likely", e, os.path.join(path,img))
            #except Exception as e:
            #    print("general exception", e, os.path.join(path,img))

create_training_data()

print(len(training_data))

import random

random.shuffle(training_data)

x = []
labels_train = []

for features,label in training_data:
    x.append(features)
    labels_train.append(label)



features_train = np.array(x).reshape(-1, 224,224,3)


def add_new_last_layer(model):
    """Add last layer to the convnet
    Args:
        base_model: keras model excluding top
        nb_classes: # of classes
    Returns:
        new keras model with last layer
    """
    model.add(GlobalAveragePooling2D())
    model.add(Dense(128, activation='relu'))  #new FC layer, random init
    model.add(Dense(32, activation='relu'))  #new FC layer, random init
    model.add(Dense(6, activation='softmax')) #new softmax layer
    
    return (model)


def setup_to_transfer_learn(model, base_model):
    """Freeze all layers and compile the model"""
    for layer in base_model.layers:
        layer.trainable = False
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])


def train():
    #import ipdb; ipdb.set_trace()
    nb_classes = 6
    nb_epoch = int(input("Input epochs"))
    batch_size = int(input("Input batch size"))

    # train_paths, test_paths, valid_paths = get_data_paths()

    # print(f"No. of Train samples = {len(train_paths)} \n")
    # print(f"No. of Test samples = {len(test_paths)} \n")
    # print(f"No. of Valid samples = {len(valid_paths)} \n")

    # train_labels = get_labels(train_paths)
    # print(f'For Train = {Counter(train_labels)} \n')
    # train_labels = np.asarray(one_hot_encoding(train_labels))

    # test_labels = get_labels(test_paths)
    # print(f'For Test = {Counter(test_labels)} \n')
    # test_labels = np.asarray(one_hot_encoding(test_labels))

    # valid_labels = get_labels(valid_paths)
    # print(f'For Valid = {Counter(valid_labels)} \n')
    # valid_labels = np.asarray(one_hot_encoding(valid_labels))

    # train_images = get_images(train_paths)
    # test_images = get_images(test_paths)
    # valid_images = get_images(valid_paths)

    # setup model
    base_model = MobileNet(input_shape=(224, 224, 3),
        weights='imagenet', include_top=False) 
    
    new_model = Sequential()
    new_model.add(base_model)
    model = add_new_last_layer(new_model)

    #    for i, layer in enumerate(model.layers):
    #        print(i, layer.name)

    #    import ipdb; ipdb.set_trace()
    for layer in base_model.layers:
        layer.trainable = False
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

    #import ipdb; ipdb.set_trace()
    # weight_train_labels = [np.argmax(r) for r in train_labels]
    # weights = class_weight.compute_class_weight(
    #     'balanced', np.unique(weight_train_labels), y=weight_train_labels)
    # class_weights = {0: weights[0], 1: weights[1]}

    history = model.fit(
        x=features_train,
        y=labels_train,
        batch_size=batch_size,
        epochs=int(nb_epoch),
        verbose=1,
        shuffle=True,
        validation_split=0.3)

    model.save('new.model')

    # y_pred_class = model.predict(test_images, verbose=1)

    # y_pred_class = [np.argmax(r) for r in y_pred_class]
    # test_y = [np.argmax(r) for r in test_labels]

    # print('Confusion matrix is \n', confusion_matrix(test_y, y_pred_class))
    # print(confusion_matrix(test_y, y_pred_class).ravel())
    
    

    ft_epochs=int(input('Please input your fine tuning epochs'))

    fine_tune(model)
    history = model.fit(
            x=features_train,
            y=labels_train,
            batch_size=batch_size,
            epochs=int(ft_epochs),
            verbose=1,
            shuffle=True,
            validation_split=0.3)

    model.save('new_ft.model')

    # print('_______Results After Fine Tuning____________')
    # y_pred_class = model.predict(test_images, verbose=1)

    # y_pred_class = [np.argmax(r) for r in y_pred_class]
    # test_y = [np.argmax(r) for r in test_labels]

    # print('Confusion matrix is \n', confusion_matrix(test_y, y_pred_class))
    # print(confusion_matrix(test_y, y_pred_class).ravel())

train()