# -*- coding: utf-8 -*-
"""Transfer Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ix-7TSW5kqI4Jh9DRNI3_JR4FwEjLdKu
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import cv2
import tensorflow as tf
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Flatten, BatchNormalization, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
import itertools
import os
import os.path
import shutil
import random
import glob
import matplotlib.pyplot as plt
import warnings
import os 
import xml.etree.ElementTree as ET
from collections import OrderedDict
import PIL
from PIL import Image
warnings.simplefilter(action='ignore', category=FutureWarning)
# %matplotlib inline

from google.colab import drive
drive.mount('/content/gdrive')

!pwd

!tar -xvf "/content/gdrive/MyDrive/VOCtrainval_11-May-2012.tar" -C "/content/"

def parseXML(tree):
  roww = OrderedDict()
  for elements in tree.iter():
    if elements.tag == 'filename':
      roww['{}'.format(elements.tag)] = str(elements.text)
    if elements.tag =='object':
      for element in elements:
        if element.tag == 'name':
          roww['{}'.format(element.tag)] = str(element.text)
  return roww

df_annot = []
for file in os.listdir('/content/VOCdevkit/VOC2012/Annotations'):
  if file.startswith('.') == 0:
    tree = ET.parse(os.path.join('/content/VOCdevkit/VOC2012/Annotations', file))
    roww = parseXML(tree)
    df_annot.append(roww)

  df_annotation = pd.DataFrame(df_annot)

df_annotation

list_of_unique_class =df_annotation['name'].unique()
list_of_files = df_annotation['filename'].unique()
annotations_list = df_annotation.values.tolist()

list_of_unique_class

annotations_list

os.chdir('/content/VOCdevkit/VOC2012/JPEGImages')
if os.path.isdir('train/person') is False:
  for class_name in list_of_unique_class:
    os.makedirs('train/{}'.format(class_name))
    os.makedirs('validation/{}'.format(class_name))

  for index, i in enumerate(annotations_list):
    if index %4 !=0:
      shutil.move(i[0], 'train/{}'.format(i[1]))
    if index %4 == 0:
      shutil.move(i[0], 'validation/{}'.format(i[1]))

  os.chdir('/../..')

train_path = '/content/VOCdevkit/VOC2012/JPEGImages/train'
validation_path = '/content/VOCdevkit/VOC2012/JPEGImages/validation'

train_batches = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)\
.flow_from_directory(train_path, target_size= (224,224), batch_size = 128, class_mode = 'categorical')

valid_batches = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)\
.flow_from_directory(validation_path, target_size= (224,224), batch_size = 128, class_mode = 'categorical')

vgg16_model = tf.keras.applications.vgg16.VGG16()

model = Sequential()
for layer in vgg16_model.layers[:-1]:
    model.add(layer)


for layer in model.layers:
  layer.trainable = False

model.add(Dense(20, activation = 'softmax'))

model.summary()

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x=train_batches,
          steps_per_epoch=len(train_batches),
          validation_data=valid_batches,
          validation_steps=len(valid_batches),
          epochs=15,
          verbose=2)

!pwd

os.chdir('/content/')

model.save('trained_model.h5')

model.save('/content/gdrive/MyDrive/models/',save_format= 'tf')