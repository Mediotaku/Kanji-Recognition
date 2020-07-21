import struct
import os
import json
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

load_images_to_data('./open_dataset/mnist')