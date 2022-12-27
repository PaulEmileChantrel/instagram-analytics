import pandas as pd
import requests
import shutil

df = pd.read_csv('gresunstudio.csv')
df = df.sort_values(by='media',ignore_index=True)
img_links = df['img_url']

# function to download an image given an img_link and save it to a file_name
def download_img(img_link,file_name):

    res = requests.get(img_link,stream=True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')


# Download every image in the csv file
for i in range(df.shape[0]):
    file_name = 'img/image'+str(i)+'.jpg'
    print(img_links[i])
    download_img(img_links[i],file_name)
