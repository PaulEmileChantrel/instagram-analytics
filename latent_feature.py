import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt
num_classes = 3
# Load the pre-trained model
model =tf.keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/feature_vector/5",
                   trainable=False),  # Can be True, see below.
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
model.build([None, 224, 224, 3])
# Load the VGG19 model from TensorFlow Hub
#model = hub.load('https://tfhub.dev/google/imagenet/vgg19/feature_vector/4')

model.summary()


# Create the figure and subplot
fig, ax = plt.subplots()
#Load the image file
for i in range(33):
    path = f'img/image{i}.jpg'
    image = tf.keras.preprocessing.image.load_img(path, target_size=(224, 224))

    # Convert the image to a numpy array
    image_array = tf.keras.preprocessing.image.img_to_array(image)

    # Reshape the array to match the model's input shape
    image_array = image_array.reshape((1, 224, 224, 3))

    # Normalize the pixel values
    image_array = image_array / 255.0

    # Use the model to make a prediction
    prediction = model.predict(image_array)

    # Get the latent features from the model's output layer
    latent_features = model.output

    # Create a new model that outputs the latent features
    latent_model = tf.keras.Model(inputs=model.input, outputs=latent_features)

    # Extract the latent features from the image
    latent_features = latent_model.predict(image_array)
    print(latent_features)
    #latent_features_list.append(latent_features)

    #plot image
    image = plt.imread(path)

    x = latent_features[0,0]*50
    y = latent_features[0,1]*50
    print(x,y)
    # Plot the image on the subplot
    ax.imshow(image, extent=[x, x+5, y, y+5])

    # Plot the x and y data as points
    ax.scatter(x, y,marker = None)

plt.show()
