import pandas as pd
import requests
import shutil

df = pd.read_csv('gresunstudio_2.csv')

img_links = df['15']


def download_img(img_link,file_name):
    res = requests.get(img_link,stream=True)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

for i in range(df.shape[0]):
    file_name = 'img/image'+str(i)+'.png'
    print(img_links[i])
    download_img(img_links[i],file_name)
