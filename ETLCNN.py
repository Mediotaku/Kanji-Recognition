import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.utils import np_utils
from ETLtest import KerasHiragana
from ETLtest import KerasKanji
from OpenDataset import load_images_to_data
import matplotlib.pyplot as plt
import numpy as np
#This test is working on Python 2.7.17

# load data from ETL hiragana
X_train, y_train, X_test, y_test = KerasKanji(160,0.2)

"""
X_train = X_train.reshape(X_train.shape[0], 64, 64, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 64, 64, 1).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

"""
num_classes = y_test.shape[1]
#num_pixels = X_train.shape[1] * X_train.shape[2]
print(num_classes)
def baseline_model():
	# create model
	model = Sequential()
	#Entrada (pixeles de la imagen)
	model.add(Dense(4096, input_dim=4096, kernel_initializer='normal', activation='relu'))

	#model.add(Dense(512, kernel_initializer='normal', activation='relu'))
	#model.add(Dropout(0.2))
	#model.add(Dense(256, kernel_initializer='normal', activation='relu'))
	#model.add(Dropout(0.2))

	#Modelo dividido en dos hidden layers con baseline error of 1.79%
	#model.add(Dense(150, kernel_initializer='normal', activation='relu'))
	#model.add(Dense(150, kernel_initializer='normal', activation='relu'))

	
	model.add(Dense(1000, kernel_initializer='normal', activation='relu'))
	model.add(BatchNormalization())
	model.add(Dropout(0.5))
	#model.add(Dense(1820, kernel_initializer='normal', activation='relu'))
	#model.add(BatchNormalization())
	#model.add(Dropout(0.5))

	#Salida (10 characters)
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	#model.compile(loss='categorical_crossentropy',  optimizer=keras.optimizers.SGD(lr=learning_rate, momentum=0.8, decay=decay_rate), metrics=['accuracy'])
	model.compile(loss='categorical_crossentropy',  optimizer="adam", metrics=['accuracy'])
	return model

def cnn_model():
	# create model
	model = keras.Sequential()
	model.add(keras.Input(shape=(64, 64, 1)))
	model.add(layers.Conv2D(32, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D(pool_size=(2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D(pool_size=(2, 2)))
	model.add(layers.Flatten())
	model.add(layers.Dropout(0.5))
	model.add(layers.Dense(num_classes, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

#Plot accuracy and val_accuracy into graph
def show_history(history, scores):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train_accuracy', 'validation_accuracy'], loc='best')
    plt.title("Baseline Error: %.2f%%" % (100-scores[1]*100))
    plt.show()

# build the model
#model = baseline_model()
model = cnn_model()
# Fit the model
result = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=128, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))
show_history(result, scores)

