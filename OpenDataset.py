import struct
import os
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.utils import np_utils
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from keras.utils import np_utils
from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

#Script to create our own open dataset 

def load_images_to_data(image_directory, test_size=0.2):

    with open('./Kanji_app/CharacterJSON.json', encoding="utf8") as f:
        classes = json.load(f)

    X=[]
    Y=[]
    list_of_files = os.listdir(image_directory)
    for file in list_of_files:
        image_file_name = os.path.join(image_directory, file)
        if ".png" in image_file_name:
            img = Image.open(image_file_name).convert("L")
            shapes= 28, 28
            outData = np.asarray(img.getdata()).reshape(shapes[0], shapes[1])
            X.append(outData)
            Y.append(classes["character"].index(image_file_name[21]))
    
    X, Y= np.asarray(X, dtype=np.int32), np.asarray(Y, dtype=np.int32)
    characters=X
    labels=Y

    unique_labels= list(set(labels))
    labels_dict= {unique_labels[i]: i for i in range(len(unique_labels))}
    new_labels= np.array([labels_dict[l] for l in labels],dtype=np.int32)

    characters_shuffle, new_labels_shuffle = shuffle(characters, new_labels, random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(characters_shuffle, new_labels_shuffle, test_size=test_size, random_state=42)

    #(28, 28, 1)

    num_pixels = x_train.shape[1] * x_train.shape[2]
    X_train=  x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32')
    X_test= x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32')

    # normalize inputs from 0-255 to 0-1
    X_train = X_train / 255
    X_test = X_test / 255
    
    nb_classes= len(unique_labels)
    Y_train= np_utils.to_categorical(y_train, nb_classes)
    Y_test= np_utils.to_categorical(y_test, nb_classes)

    return X_train, Y_train, X_test, Y_test


# load data from OpenDataset
X_train, y_train, X_test, y_test = load_images_to_data('./open_dataset/touch')

num_classes = y_test.shape[1]
#num_pixels = X_train.shape[1] * X_train.shape[2]
print(num_classes)
def baseline_model():
	# create model
	model = Sequential()
	#Entrada (pixeles de la imagen)
	model.add(Dense(784, input_dim=4096, kernel_initializer='normal', activation='relu'))

	model.add(Dense(522, kernel_initializer='normal', activation='relu'))
	model.add(BatchNormalization())
	model.add(Dropout(0.5))

	#Salida 
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	#model.compile(loss='categorical_crossentropy',  optimizer=keras.optimizers.SGD(lr=learning_rate, momentum=0.8, decay=decay_rate), metrics=['accuracy'])
	model.compile(loss='categorical_crossentropy',  optimizer="adam", metrics=['accuracy'])
	return model

def cnn_model():
	# create model
	model = keras.Sequential()
	model.add(keras.Input(shape=(28, 28, 1)))
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

def CNN_deep_model():
	model = keras.Sequential()
	model.add(keras.Input(shape=(28, 28, 1)))
	model.add(layers.Conv2D(32, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D(pool_size=(2, 2)))
	model.add(layers.Dropout(0.25))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D(pool_size=(2, 2)))
	model.add(layers.Dropout(0.25))
	model.add(layers.Conv2D(128, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D(pool_size=(2, 2)))
	model.add(layers.Dropout(0.25))
	model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
	model.add(layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
	model.add(layers.Dropout(0.25))

	model.add(layers.Flatten())
	model.add(layers.Dense(4096))
	model.add(layers.Activation('relu'))
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
#model = cnn_model()
model = CNN_deep_model()
# Fit the model
result = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=16, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))
show_history(result, scores)

#img = X_train[0]
#img_class = model.predict_classes(img.reshape((1, 28, 28, 1)))
#prediction = img_class[0]
#classname = img_class[0]
#print("Class: ",classname)
#img = img.reshape((28,28))
#plt.imshow(img)
#plt.title(classname)
#plt.show()