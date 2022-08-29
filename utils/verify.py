import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics.pairwise import cosine_similarity
import os
import cv2


def load_image(image_path):
    # Return the image in the format required by VGG16 model.
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def extract_features(feature_extractor, image):
    # Returns the features extracted by the model.
    return feature_extractor.predict(load_image(image))

def cosine_similarity_fn(anchor_image_feature, test_image_feature):
    # Returns the features extracted by the model.
    return cosine_similarity(anchor_image_feature, test_image_feature)[0][0]


def verify(img_1, img_2):
    vgg_model = tf.keras.models.load_model('models/vgg16')
    feature_extractor = tf.keras.Sequential(vgg_model.layers[:-1])
    img_1_features = extract_features(feature_extractor, img_1)
    img_2_features = extract_features(feature_extractor, img_2)
    
    return str(round(cosine_similarity_fn(img_1_features, img_2_features), 3))