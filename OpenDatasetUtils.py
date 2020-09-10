import struct
import os
import json
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from answers import mouse
from answers import touch

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def preprocessing(image_directory):
    list_of_files = os.listdir(image_directory)
    for file in list_of_files:
        image_file_name = os.path.join(image_directory, file)
        if ".png" in image_file_name:
            img = Image.open(image_file_name).convert("L")
            gray = cv_imread(image_file_name)
            gray = cv2.bitwise_not(gray)
            filename = './open_dataset/black/'+image_file_name.split('\\')[1]
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, gray, None)
            with open(filename, "wb") as f:
                n.tofile(f)

def create_image(image_directory):
    images_outers= []
    list_of_files = os.listdir(image_directory)
    images = []
    i = 0
    for file in list_of_files:
        image_file_name = os.path.join(image_directory, file)
        if "20" in image_file_name:
            image = Image.open(image_file_name).convert("L")
            #image = image.resize((50,50), Image.ANTIALIAS)
            images.append(image)
            i = i + 1
        if i == 20:
            image_outer = np.hstack(images)
            images_outers.append(image_outer)
            images = []
            i = 0
    new_img = np.vstack(images_outers)
    new_image = Image.fromarray(new_img)
    new_image.save('./open_dataset/examples.png')
    
def pie_char():
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

    labels = 'Japan', 'Others'
    sizes = [326, 1811]
    plt.pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title('Where are you from?')

    plt.savefig('./open_dataset/country.png')
    plt.clf()
    labels = 'Native', 'Second language', 'Student'
    sizes = [329, 2, 1806]
    plt.pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title('What is your level of Japanese language?')

    plt.savefig('./open_dataset/language.png')
    plt.clf()
    labels = 'Mouse', 'Finger', 'Stylus pen'
    sizes = [1453, 639, 45]
    plt.pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title('What have you used to write the character?')

    plt.savefig('./open_dataset/type.png')
    plt.clf()

#pie_char()
#create_image('./open_dataset/black')            
#preprocessing('./open_dataset/mnist')

def transfer(image_directory):
    list_of_files = os.listdir(image_directory)
    for file in list_of_files:
        image_file_name = os.path.join(image_directory, file)
        #print(image_file_name)
        if image_file_name in touch:
            img = cv_imread(image_file_name)
            filename = './open_dataset/touch/'+image_file_name.split('\\')[1]
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, None)
            with open(filename, "wb") as f:
                n.tofile(f)

transfer('./open_dataset/black')