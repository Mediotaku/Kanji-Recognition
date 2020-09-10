import struct
from PIL import Image
import numpy as np
from keras.utils import np_utils
from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
#This test is working on Python 2.7.17
#Notes for Python 3 use: must solve problem regading "encoding" parameter
#in open function, which must be included when using this version

#Here we read the database as indicated by the ETL
def read_record_ETL8B2(f):
    s = f.read(512)
    r = struct.unpack('>2H4s504s', s)
    i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
    return r + (i1,)



#Here we get the data using read_record with the correct parameters
#categories-> classes
#writers-> examples per class
def get_ETL8B2(dataset, categories, writers):
    filename = 'ETL8B/ETL8B2C'+ str(dataset)
    #Creating one kanji image, then we will create a dataset for keras with them
    new_img = Image.new('1', (64, 64))

    iter(categories)
    X = []
    Y = []
    scriptTypes = []

    for id_category in categories:
        with open(filename, 'rb') as f:  #For Python 3, we have to use 'rb' mode for reading in binary
            f.seek((id_category * 160 + 1) * 512) #In case of ETL8B2C dataset
            for i in range(writers):
                r = read_record_ETL8B2(f)
                new_img.paste(r[-1], (0,0))
                #Image.eval applies a function to each pixel of the given image
                iI = Image.eval(new_img, lambda x: not x)

                #Formating id_category and i into string to create 
                #a filename for every writer from each class (avoiding overwrite)
                #fn = 'ETL8B/ETL8B2_{:s}.png'.format(str(id_category)+"_"+str(i))
                #iI.save(fn, 'PNG')

                shapes= 64, 64
                outData = np.asarray(iI.getdata()).reshape(shapes[0], shapes[1])

                X.append(outData)
                Y.append(r[1])
                if(id_category<75):
                    scriptTypes.append(0)
                else:
                    scriptTypes.append(2)

    output=[]
    X, Y= np.asarray(X, dtype=np.int32), np.asarray(Y, dtype=np.int32)
    output+= [X]
    output+= [Y]
    output+= [scriptTypes]

    return output

#Adapt for Keras processing
"""
    writer->writers per hiragana class
    test_size->fraction of data to obtain a test error (which percentage is used for a test set)
"""
def KerasHiragana(writers=160,test_size=0.2):
    #We have a total of 75 hiragana classes and 160 writers per class
    char, labs, spts= get_ETL8B2(1, range(0, 75), 160)
    characters=char
    labels=labs
    scripts= spts
    print(len(characters[1]))

    unique_labels= list(set(labels))
    labels_dict= {unique_labels[i]: i for i in range(len(unique_labels))}
    new_labels= np.array([labels_dict[l] for l in labels],dtype=np.int32)

    
    #Shuffle first
    characters_shuffle, new_labels_shuffle = shuffle(characters, new_labels, random_state=0)
    #Split dataset to hold out part of it for a test set
    #test_size must be input with the key word because if a number is used, train_test_split
    #will consider it as another array to split(the function can split any number of arrays),
    #but as this is a float, not an array, an error will rise
    x_train, x_test, y_train, y_test = train_test_split(characters_shuffle, new_labels_shuffle, test_size=test_size, random_state=42)

    #(64, 64, 1)
    
    #X_train=  x_train.reshape((x_train.shape[0], 1, x_train.shape[1], x_train.shape[2]))
    #X_test= x_test.reshape((x_test.shape[0], 1, x_test.shape[1], x_test.shape[2]))
    num_pixels = x_train.shape[1] * x_train.shape[2]
    X_train=  x_train.reshape(x_train.shape[0], 64, 64, 1).astype('float32')
    X_test= x_test.reshape(x_test.shape[0], 64, 64, 1).astype('float32')

    # normalize inputs from 0-255 to 0-1
    #X_train = X_train / 255
    #X_test = X_test / 255
    
    nb_classes= len(unique_labels)
    Y_train= np_utils.to_categorical(y_train, nb_classes)
    Y_test= np_utils.to_categorical(y_test, nb_classes)

    return X_train, Y_train, X_test, Y_test


def KerasKanji(writers=160,test_size=0.2):
    #Taking samples from ETL8B2C2, where every class is a kanji. We are taking 100 classes
    char, labs, spts= get_ETL8B2(2, range(0, 100), 160) 
    characters=char
    labels=labs
    scripts= spts
    print(len(characters[1]))

    #rename labels from 0 to labels-1
    unique_labels= list(set(labels))
    labels_dict= {unique_labels[i]: i for i in range(len(unique_labels))}
    new_labels= np.array([labels_dict[l] for l in labels],dtype=np.int32)

    #Shuffle first
    characters_shuffle, new_labels_shuffle = shuffle(characters, new_labels, random_state=0)
    #Split dataset to hold out part of it for a test set
    #test_size must be input with the key word because if a number is used, train_test_split
    #will consider it as another array to split(the function can split any number of arrays),
    #but as this is a float, not an array, an error will rise
    x_train, x_test, y_train, y_test = train_test_split(characters_shuffle, new_labels_shuffle, test_size=test_size, random_state=42)

    #(1, 64, 64)
    
    #X_train=  x_train.reshape((x_train.shape[0], 1, x_train.shape[1], x_train.shape[2]))
    #X_test= x_test.reshape((x_test.shape[0], 1, x_test.shape[1], x_test.shape[2]))
    num_pixels = x_train.shape[1] * x_train.shape[2]
    print(num_pixels)
    X_train=  x_train.reshape(x_train.shape[0],64, 64, 1).astype('float32')
    X_test= x_test.reshape(x_test.shape[0],64, 64, 1).astype('float32')

    # normalize inputs from 0-255 to 0-1
    #X_train = X_train / 255
    #X_test = X_test / 255
    
    nb_classes= len(unique_labels)
    #print(nb_classes)
    Y_train= np_utils.to_categorical(y_train, nb_classes)
    Y_test= np_utils.to_categorical(y_test, nb_classes)

    return X_train, Y_train, X_test, Y_test