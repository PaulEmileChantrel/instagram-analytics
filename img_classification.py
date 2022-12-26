import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from vgg_tensorflow import vgg19_bn

# num_classes = 1001
# # Load the pre-trained model
# model =tf.keras.Sequential([
#     hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/feature_vector/5",
#                    trainable=False),  # Can be True, see below.
#     tf.keras.layers.Dense(num_classes, activation='softmax')
# ])
# model.build([None, 224, 224, 3])

model = vgg19_bn(inp_size=(224, 224, 3), pretrained=True)
# Load an image file to classify
image = tf.keras.preprocessing.image.load_img('img/image0.png', target_size=(224, 224))

# Convert the image to a numpy array
image = tf.keras.preprocessing.image.img_to_array(image)

# Add an extra dimension to the image (since the model expects a batch of images)
image = np.expand_dims(image, axis=0)

# Normalize the image pixels
image = tf.keras.applications.mobilenet.preprocess_input(image)

# Use the pre-trained model to classify the image
predictions = model.predict(image)
print(predictions)
# Print the top 5 predictions
print(predictions[0])
pred = predictions[0].argsort()[:5][::-1]
pred_pct = sorted(predictions[0])[:5][::-1]
print(predictions[0].argsort()[:5][::-1])
print(predictions[0])
# Open the file in read mode
with open('class.txt', 'r') as f:
    # Read the file into a list of lines
    lines = f.readlines()
    # Get the third line from the list
    for p,pct in zip(pred,pred_pct):
        print(f'Class {lines[p]} with {pct*100} % certainty.')
