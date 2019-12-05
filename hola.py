# Plot ad hoc mnist instances
import numpy as np
from keras.datasets import mnist
import matplotlib.pyplot as plt
from tensorflow.contrib.learn.python.learn.datasets.mnist import extract_images, extract_labels

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

# plot 4 images as gray scale
plt.subplot(221)
img = X_train[0]
img = img.reshape((28,28))
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.subplot(222)
img = X_train[1]
img = img.reshape((28,28))
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.subplot(223)
img = X_train[2]
img = img.reshape((28,28))
plt.imshow(img, cmap=plt.get_cmap('gray'))
img = X_train[3]
img = img.reshape((28,28))
plt.subplot(224)
plt.imshow(img, cmap=plt.get_cmap('gray'))
# show the plot
plt.show()