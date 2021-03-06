# importamos los modulos necesarios de keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.models import model_from_json
import matplotlib.pyplot as plt

# cargar datos de mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

print(num_pixels,num_classes)

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	#Entrada (pixeles de la imagen)
	model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))

	model.add(Dense(300, kernel_initializer='normal', activation='relu'))
	model.add(Dropout(0.5))

	#Modelo dividido en dos hidden layers con baseline error of 1.79%
	#model.add(Dense(150, kernel_initializer='normal', activation='relu'))
	#model.add(Dense(150, kernel_initializer='normal', activation='relu'))
	#Modelo de una sola hidden layer de 128
	#model.add(Dense(128, kernel_initializer='normal', activation='relu'))
	#model.add(Dropout(0.5))

	#Salida (10 digitos)
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# build the model
model = baseline_model()
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=2)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# serialize model to JSON
#model_json = model.to_json()
#with open("model.json", "w") as json_file:
#    json_file.write(model_json)
# serialize weights to HDF5
#model.save_weights("model.h5")
#print("Saved model to disk")


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
