from sys import path

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
from tensorflow_estimator.python.estimator.canned.timeseries import model

from load_image_keras.test1 import train_ds

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixels values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))



# import manual custom image

tf.keras.preprocessing.image.load_img(
    path, grayscale=False, color_mode='rgb', target_size=None,
    interpolation='nearest'
)

image = tf.keras.preprocessing.image.load_img('contoh_image.jpg')
input_arr = keras.preprocessing.image.img_to_array(image)
input_arr = np.array([input_arr])  # Convert single image to a batch.
predictions = model.predict(input_arr)

