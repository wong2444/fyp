import datetime

import numpy as np
import cv2
import pickle
import os

from PIL import Image

BASE_DIR = os.path.dirname(os.path.os.path.abspath(__file__))

cam_id = 1
face_size = (47, 62)
# monitor_winSize = (640, 480)

face_cascade = cv2.CascadeClassifier(BASE_DIR + '/cascades/data/haarcascade_frontalface_alt2.xml')
# face_cascade = cv2.CascadeClassifier('objects\\lbpcascade_frontalface.xml')


image_dir = BASE_DIR + "/images/"
recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id = 0
label_ids = {}  # {'wong':0,'chan':1}
y_labels = []
x_train = []
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            print('root', root)
            print('path', path)
            arr = os.path.basename(root).split("-")
            # label = arr[1].replace(" ", "-").lower()
            label = os.path.basename(root)
            print(label)
            # print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            # print(label_ids)
            # y_labels.append(label) # some number
            # x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
            pil_image = Image.open(path).convert("L")  # grayscale
            size = (550, 550)

            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")  # 轉換所有圖像為 numpy array
            # print(image_array)
            # faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
            # print(image_array)

            # for (x, y, w, h) in faces:
            #     roi = image_array[y:y + h, x:x + w]
            #     x_train.append(roi)
            #     y_labels.append(id_)
            x_train.append(image_array)
            y_labels.append(id_)

# print(y_labels)
# print(x_train)

with open(BASE_DIR + "\\pickles\\face-labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))  # x_train存圖片, y_labels存標籤
recognizer.save(BASE_DIR + "\\recognizers\\face-trainner.yml")
