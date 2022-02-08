from dataclasses import dataclass
from typing import List
import cv2
import os
import numpy as np
from settings import settings
from keras.models import Sequential, load_model
from sklearn.metrics import classification_report

@dataclass
class HasilAkurasi:
  label: str
  precision: float
  recall: float
  f1_score: float
  support: int

@dataclass
class Result:
  accuracy: float
  data: List[HasilAkurasi]

class Clasifier:
  labels = ['alis','baju', 'balon', 'botol', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'mata', 'meja', 'paku', 'papan', 'pohon', 'rok', 'spidol', 'tali', 'tangan', 'tas']
  classes = ['alis','baju', 'balon', 'botol', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'mata', 'meja', 'paku', 'papan', 'pohon', 'rok', 'spidol', 'tali', 'tangan', 'tas']
  img_size = 224

  def __init__(self, model_path):
    self.classes = ['alis','baju', 'balon', 'botol', 'buku', 'dasi', 'jam', 'kaca', 'kuku', 'lampu', 'mata', 'meja', 'paku', 'papan', 'pohon', 'rok', 'spidol', 'tali', 'tangan', 'tas']
    self.model = load_model(model_path)

  def parse_result(self, result) -> Result:
    data: List[HasilAkurasi] = []
    exclude = ['accuracy', 'macro avg', 'weighted avg']
    accuracy = 0
    for key, value in result.items():
      if key in exclude:
        if key == 'accuracy':
          accuracy = value
        continue
      try:
        label = self.labels.__getitem__(int(key))
        precision = round(value['precision'] * 100, 2)
        recall = round(value['recall'] * 100, 2)
        f1_score = round(value['f1-score'] * 100, 2)
        support = value['support']
        data.append(HasilAkurasi(
          label=label,
          precision=precision,
          recall=recall,
          f1_score=f1_score,
          support=support
        ))
      except BaseException as e:
        pass
    return Result(data=data, accuracy=round(accuracy * 100, 2))

  def get_data(self, files):
    data = []
    for img in files:
        try:
          # cc = img.split("_")[::-1][0].split(".")[0]
          class_num = self.labels.index(img[1])
          img_arr = cv2.imread(os.path.join('static/data_testing/', img[0]))[...,::-1] #convert BGR to RGB format
          resized_arr = cv2.resize(img_arr, (self.img_size, self.img_size)) # Reshaping images to preferred size
          data.append([resized_arr, class_num])
        except Exception:
          continue
    return np.array(data)

  def predict_all_history(self, object_path) -> Result:
    data_test = self.get_data(object_path)
    img_size = 224
    data_test = np.array(data_test, dtype=object)
    x_test, y_test = [], []
    for feature, label in data_test:
      x_test.append(feature)
      y_test.append(label)

    # Normalize the data
    x_test = np.array(x_test) / 255
    x_test.reshape(-1, img_size, img_size, 1)
    y_test = np.array(y_test)

    probs = self.model.predict([x_test])
    prediction = probs.argmax(axis=1)
    # classification report for precision, recall f1-score and accuracy
    matrix = classification_report(y_test, prediction, output_dict=True)
    return self.parse_result(matrix)

  def predict(self, object_path):

    data_test = []
    img_size = 224
    image = cv2.imread(object_path)[...,::-1]
    resized_arr = cv2.resize(image, (img_size, img_size))
    data_test.append([resized_arr, 2])
    data_test = np.array(data_test, dtype=object)
    x_test, y_test = [], []
    for feature, label in data_test:
      x_test.append(feature)
      y_test.append(label)
    x_test = np.array(x_test) / 255
    x_test.reshape(-1, img_size, img_size, 1)
    y_test = np.array(y_test)
    probs = self.model.predict([x_test])    
    prediction = probs.argmax(axis=1)
    matrix = classification_report(y_test, prediction)
    print('Classification report : \n',matrix)
    if probs[0][prediction] >= settings.Clasifier.CONF:
      return self.classes[prediction[0]]
    else:
      return 'Tidak dikenal'

    
    

# model_path="clasifier-model.h5"
# object_path='../static/4x6.jpg'

clasifier = Clasifier(settings.Clasifier.MODEL_PATH)
# result = clasifier.predict(object_path)