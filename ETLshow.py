# Plot ad hoc mnist instances
import numpy as np
from keras.datasets import mnist
import matplotlib.pyplot as plt
from ETLtest import KerasHiragana

# load Hiragana data from ETL dataset 
X_train, y_train, X_test, y_test = KerasHiragana(160,0.2)

# plot 4 images as gray scale
# adjust image size to the current setting for ETL (64,64)
plt.subplot(221)
img = X_train[0]
img = img.reshape((64,64))
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.title(X_train[0].shape[2])
plt.subplot(222)
img = X_train[1]
img = img.reshape((64,64))
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.title(X_train[1].shape[2])
plt.subplot(223)
img = X_train[2]
img = img.reshape((64,64))
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.title(X_train[2].shape[2])
img = X_train[3]
img = img.reshape((64,64))
plt.subplot(224)
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.title(X_train[3].shape[2])
# show the plot
plt.show()