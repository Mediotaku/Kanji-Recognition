# importamos los modulos necesarios de keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.models import model_from_json
import matplotlib.pyplot as plt
from tensorflow.contrib.learn.python.learn.datasets.mnist import extract_images, extract_labels
import pandas as pd

plt.rc('font', family='TakaoPGothic')

# cargar datos de mnist Kuzushiji
#(X_train, y_train), (X_test, y_test) = mnist.load_data()
with open('train-images-idx3-ubyte.gz', 'rb') as f:
  X_train = extract_images(f)
with open('train-labels-idx1-ubyte.gz', 'rb') as f:
  y_train = extract_labels(f)

with open('t10k-images-idx3-ubyte.gz', 'rb') as f:
  X_test = extract_images(f)
with open('t10k-labels-idx1-ubyte.gz', 'rb') as f:
  y_test = extract_labels(f)

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

#Read CSV with Hiragana labels and create array
data = pd.read_csv("kmnist_classmap.csv") 
hira_labels= data['codepoint'].values

json_file = open('model_hiragana.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model_hiragana.h5")
print("Loaded model from disk")

img = X_train[4]
testimg = img.reshape((1,784))
img_class = model.predict_classes(testimg)
prediction = img_class[0]
classname = hira_labels[img_class[0]]
print("Class: ",classname)
img = img.reshape((28,28))
plt.imshow(img)
plt.title(classname)
plt.show()