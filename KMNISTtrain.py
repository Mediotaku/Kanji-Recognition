# importamos los modulos necesarios de keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.utils import np_utils
from keras.models import model_from_json
import matplotlib.pyplot as plt
import numpy as np

# cargar datos de mnist Kuzushiji
#(X_train, y_train), (X_test, y_test) = mnist.load_data()
#En formato .npz de numpy
X_train = np.load('kmnist-train-imgs.npz')['arr_0']
y_train = np.load('kmnist-train-labels.npz')['arr_0']
X_test = np.load('kmnist-test-imgs.npz')['arr_0']
y_test = np.load('kmnist-test-labels.npz')['arr_0']

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape((X_train.shape[0], 28, 28, 1)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1)).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

print(num_pixels,num_classes)

learning_rate = 1e-3
epochs = 50
decay_rate = learning_rate / epochs

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	#Entrada (pixeles de la imagen)
	model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))

	model.add(Dense(512, kernel_initializer='normal', activation='relu'))
	#model.add(Dropout(0.2))
	model.add(Dense(256, kernel_initializer='normal', activation='relu'))
	#model.add(Dropout(0.2))

	#Modelo dividido en dos hidden layers con baseline error of 1.79%
	#model.add(Dense(150, kernel_initializer='normal', activation='relu'))
	#model.add(Dense(150, kernel_initializer='normal', activation='relu'))

	#Modelo de una sola hidden layer de 128
	#model.add(Dense(522, kernel_initializer='normal', activation='relu'))
	#model.add(Dropout(0.5))

	#Salida (10 characters)
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	#model.compile(loss='categorical_crossentropy',  optimizer=keras.optimizers.SGD(lr=learning_rate, momentum=0.8, decay=decay_rate), metrics=['accuracy'])
	model.compile(loss='categorical_crossentropy',  optimizer="adam", metrics=['accuracy'])
	return model

def CNN_model():
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


#Simple prediction
def predict():
	img = X_train[0]
	testimg = img.reshape((1,784))
	img_class = model.predict_classes(testimg)
	prediction = img_class[0]
	classname = img_class[0]
	print("Class: ",classname)
	img = img.reshape((28,28))
	plt.imshow(img)
	plt.title(classname)
	plt.show()

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
model = CNN_model()
# Fit the model
result = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=128, epochs=20, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=2)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))
show_history(result, scores)

# serialize model to JSON
model_json = model.to_json()
with open("model_hiraganaadam.json", "w") as json_file:
    json_file.write(model_json)
#serialize weights to HDF5
model.save_weights("model_hiraganaadam.h5")
print("Saved model to disk")

