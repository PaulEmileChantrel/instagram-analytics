# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
#from imutils import paths
import numpy as np
#import argparse
import imutils
import cv2
import matplotlib.pyplot as plt
import pandas as pd

def plot_rms(x_list,y_list,path_list):
  # Extract the x and y coordinates from the rms_values list
  # x_list = [rms[0] for rms in rms_values]
  # y_list = [rms[1] for rms in rms_values]
  # path_list = [rms[2] for rms in rms_values]


  # Create the figure and subplot
  plt.figure(0)
  fig1, ax1 = plt.subplots()
  plt.figure(1)
  fig, ax2 = plt.subplots()
  for x,y,path,color in zip(x_list,y_list,path_list,norm_likes_log):

      x = np.mean(x)
      y = np.mean(y)*10000
      print(x,y)
      image = plt.imread(path)
      image_height, image_width = image.shape[:2]

      ax1.imshow(image,  extent=[x,x+15*color, y,y+15*color])
      # Create a scatter plot using the x and y coordinates
      # Plot the x and y data as points
      ax1.scatter(x, y, marker=",",color='white',alpha=0)
      ax2.scatter(x, y,color = [color,0,1-color])
  ax1.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
  ax1.yaxis.label.set_color('white')          #setting up Y-axis label color to blue

  ax1.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
  ax1.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black

  ax1.spines['left'].set_color('white')        # setting up Y-axis tick color to red
  ax1.spines['top'].set_color('white')
  fig1.savefig('knn_images.png', transparent=True)

def image_to_feature_vector(image, size=(32, 32)):
	# resize the image to a fixed size, then flatten the image into
	# a list of raw pixel intensities
	return cv2.resize(image, size).flatten()

def extract_color_histogram(image, bins=(8, 8, 8)):
	# extract a 3D color histogram from the HSV color space using
	# the supplied number of `bins` per channel
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv], [0, 1, 2], None, bins,
		[0, 180, 0, 256, 0, 256])
	# handle normalizing the histogram if we are using OpenCV 2.4.X
	if imutils.is_cv2():
		hist = cv2.normalize(hist)
	# otherwise, perform "in place" normalization in OpenCV 3 (I
	# personally hate the way this is done
	else:
		cv2.normalize(hist, hist)
	# return the flattened histogram as the feature vector
	return hist.flatten()

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
# ap.add_argument("-k", "--neighbors", type=int, default=1,help="# of nearest neighbors for classification")
# ap.add_argument("-j", "--jobs", type=int, default=-1, help="# of jobs for k-NN distance (-1 uses all available cores)")
# args = vars(ap.parse_args())

# grab the list of images that we'll be describing
print("[INFO] describing images...")
#imagePaths = list(paths.list_images(args["dataset"]))
# initialize the raw pixel intensities matrix, the features matrix,
# and labels list
rawImages = []
features = []
filenames = []

num_of_images = 342
# loop over the input images
for i in range(num_of_images):
    imagePath = f'img/image{i}.jpg'
	# load the image and extract the class label (assuming that our
	# path as the format: /path/to/dataset/{class}.{image_num}.jpg
    image = cv2.imread(imagePath)
    #label = imagePath.split(os.path.sep)[-1].split(".")[0]
    # extract raw pixel intensity "features", followed by a color
    # histogram to characterize the color distribution of the pixels
    # in the image
    pixels = image_to_feature_vector(image)
    hist = extract_color_histogram(image)
    # update the raw images, features, and labels matricies,
    # respectively
    rawImages.append(pixels)
    features.append(hist)
    filenames.append(imagePath)
    # show an update every 1,000 images
    #if i > 0 and i % 1 == 0:
    print("[INFO] processed {}/{}".format(i+1, num_of_images))

# show some information on the memory consumed by the raw images
# matrix and features matrix
rawImages = np.array(rawImages)
features = np.array(features)
filenames = np.array(filenames)
print("[INFO] pixels matrix: {:.2f}MB".format(
	rawImages.nbytes / (1024 * 1000.0)))
print("[INFO] features matrix: {:.2f}MB".format(
	features.nbytes / (1024 * 1000.0)))

df = pd.read_csv('gresunstudio_translated.csv')
likes = np.array(list(df['likes']))
print(likes.shape)
likes_log = np.sqrt(likes)
norm_likes_log = (likes_log - np.min(likes_log))/(np.max(likes_log)- np.min(likes_log))

rawImages = np.mean(rawImages,axis=1)
features = np.mean(features,axis=1)
print(rawImages.shape,norm_likes_log.shape)
df_img = pd.DataFrame({'rawImages':rawImages,'features':features,'filenames':filenames,'likes':likes,'norm_likes':norm_likes_log})
df_img.to_csv('knn_images.csv')
plot_rms(rawImages,features,filenames)
plt.show()
