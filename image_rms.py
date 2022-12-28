from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('gresunstudio_translated.csv')
likes = np.array(list(df['likes']))
likes_log = np.log(likes)
norm_likes_log = (likes_log - np.min(likes_log))/(np.max(likes_log)- np.min(likes_log))
def get_H(file_name):
    reference_image_1 = Image.open(file_name)
    reference_image_arr = np.asarray(reference_image_1)
    #print(np.shape(reference_image_arr))

    flat_array_1 = reference_image_arr.flatten()
    RH1 = Counter(flat_array_1)

    H1 = []
    for i in range(256):
        if i in RH1.keys():
            H1.append(RH1[i])
        else:
            H1.append(0)
    return H1

def L2Norm(H1,H2):
    distance =0
    for i in range(len(H1)):
        distance += np.square(H1[i]-H2[i])
    return np.sqrt(distance)
img1 = get_H('img/image1.jpg')
img2 =  get_H('img/image2.jpg')
img3 = get_H('img/image0.jpg')
# dist_test_ref_1 = L2Norm(H1,test_H)
# print("The distance between Reference_Image_1 and Test Image is : {}".format(dist_test_ref_1))
# dist_test_ref_1 = L2Norm(H1,H2)
# print("The distance between Reference_Image_1 and Test Image is : {}".format(dist_test_ref_1))
#
# dist_test_ref_2 = L2Norm(H2,test_H)
# print("The distance between Reference_Image_2 and Test Image is : {}".format(dist_test_ref_2))

ref1 = 'img/image0.jpg'
ref2 = 'img/image313.jpg'#we take images that are far away from each other

filenames = [f'img/image{i}.jpg' for i in range(262)]
rms1 = [L2Norm(get_H(ref1), get_H(img)) for img in filenames]
rms2 = [L2Norm(get_H(ref2), get_H(img)) for img in filenames]

def plot_rms(x_list,y_list,path_list):
  # Extract the x and y coordinates from the rms_values list
  # x_list = [rms[0] for rms in rms_values]
  # y_list = [rms[1] for rms in rms_values]
  # path_list = [rms[2] for rms in rms_values]


  # Create the figure and subplot
  plt.figure(0)
  fig, ax1 = plt.subplots()
  plt.figure(1)
  fig, ax2 = plt.subplots()
  for x,y,path,color in zip(x_list,y_list,path_list,norm_likes_log):
      print(x,y)
      image = plt.imread(path)
      ax1.imshow(image, extent=[x, x+100000, y, y+100000])
      # Create a scatter plot using the x and y coordinates
      # Plot the x and y data as points
      ax1.scatter(x, y, marker=",",color='white',alpha=0)
      ax2.scatter(x, y,color = [color,0,1-color])

plot_rms(rms1,rms2,filenames)


plt.show()
