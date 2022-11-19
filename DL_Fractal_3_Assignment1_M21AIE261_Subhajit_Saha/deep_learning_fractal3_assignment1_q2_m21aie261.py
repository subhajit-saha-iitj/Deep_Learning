# -*- coding: utf-8 -*-
"""Deep_Learning_Fractal3_Assignment1_Q2_M21AIE261.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tBb2eqqkbOvI0nCvmhfsjPZH2u-Df9jJ
"""

## Deep Learning
## Fractal 3 - Assignment 1
## Subhajit Saha - M21AIE261

## Q2: implement denoising AE (using AE from first question, convert into D-AE) and compare with inbuilt D-AE. (using MNIST database)

##!pip install tensorflow

## Importinh required modules
import numpy as np 
import pandas as pd

# Input data files are available in the "../input/" directory.

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

#Importing all the dependencies
import tensorflow as tf
# from keras.backend.tensorflow_backend import set_session
from keras.backend import set_session
import keras
from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, Dense, Input, Reshape, Flatten, Lambda, Conv2DTranspose,UpSampling2D
from keras.preprocessing import backend as K
import matplotlib.pyplot as plt
import numpy as np
from keras.datasets import mnist
from keras import optimizers

# download training and test data from mnist and reshape it

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
X_train = X_train.astype('float32') / 255.
output_X_train = X_train.reshape(-1,28,28,1)

X_test = X_test.astype('float32') / 255.
output_X_test = X_test.reshape(-1,28,28,1)

print(X_train.shape, X_test.shape)

# adding some noise to data

input_x_train = output_X_train + 0.5 * np.random.normal(loc=0.0, scale=1.0, size=output_X_train.shape) 
input_x_test = output_X_test + 0.5 * np.random.normal(loc=0.0, scale=1.0, size=output_X_test.shape)

input_img = Input(shape=(28, 28, 1))  # adapt this if using `channels_first` image data format

x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

# at this point the representation is (7, 7, 32)

x = Conv2D(32, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

## implementing denoising AE (using AE from first question, convert into D-AE) and compare with inbuilt D-AE. (using MNIST database)

autoencoder = Model(input_img, decoded)
m = 128
n_epoch = 50
adam = optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
autoencoder.compile(optimizer=adam, loss='binary_crossentropy',metrics=['accuracy'])
hist = autoencoder.fit(input_x_train,output_X_train, epochs=n_epoch, batch_size=m, shuffle=True,validation_split=0.20)

