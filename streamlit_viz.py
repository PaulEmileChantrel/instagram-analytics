import streamlit as st
import pandas as pd
#from process_data import *
import altair as alt
import matplotlib.pyplot as plt
import base64
# Page settings
st.set_page_config(page_title='IG Analytics',page_icon=":bar_chart:",layout="wide")

# Loading the dataframe file
df = pd.read_csv('gresunstudio_translated.csv')
df_key_word = pd.read_csv('key_words.csv')
print(df.shape[0])

#df = preformat(df)


# -- SIDEBARS --#
st.sidebar.header("Please filter here :")
#
# work_types = st.sidebar.multiselect(
#     "Select a type of work:",
#     options = df['work_type'].unique(),
#     default = df['work_type'].unique()
# )
n1 = st.sidebar.slider('Number of posts',min_value=4,max_value=28,value=8)  # 👈 this is a widget
n2 = st.sidebar.slider('Number of key words',min_value=4,max_value=28,value=8)  # 👈 this is a widget
n3 = st.sidebar.slider('Number of key words (avg)',min_value=4,max_value=28,value=8)  # 👈 this is a widget
x = st.sidebar.slider('Number of most liked posts shown',min_value=4,max_value=28,value=8)  # 👈 this is a widget
#
# df_selection = df.query(
#     "work_type == @work_types"
# )
# df_selection.reset_index(drop=True,inplace=True)




# # Loading all the df
# companies_df,via_df,job_title_df,key_df,work_df,schedule_type_df=process_data(df_selection)
# companies_df = companies_df[:n1]
# via_df = via_df[:n2]
# job_title_df = job_title_df[:n3]

## -- Page --
st.title(':bar_chart: IG Data Analyst for Gresun Studio')
st.markdown("##")


number_of_likes = sum(list(df['likes']))
avg_number_of_likes = number_of_likes/df.shape[0]
left,right = st.columns(2)
with left:
    st.subheader(f'Total likes : {number_of_likes}❤️!')
    st.subheader(f'Average likes per posts : {avg_number_of_likes:0.2f}❤️!')

st.markdown('---')


left,right = st.columns(2)
# Like accross time
likes_df = df[['likes']]
likes_df.index = df['date']
#companies_df.rename(columns={'company_name':'Company Name'},inplace=True)
with left :
    st.write('Likes across time')
    st.line_chart(likes_df)

# Most liked posts
df['index'] = df.index
most_liked_df = df[['index','likes']]
most_liked_df = most_liked_df.astype({"index":str,"likes":int})

most_liked_df = most_liked_df.sort_values(by="likes",ascending=False)
most_liked_df = most_liked_df.iloc[:n1]
# image_paths = [f'img/image{i}.jpg' for i in range(8)]
# encoded_images = [base64.b64encode(open(path, 'rb').read()).decode() for path in image_paths]
# most_liked_df['Image'] = encoded_images
# st.dataframe(most_liked_df)
with right :
    st.write('Most liked Posts')
    st.altair_chart(alt.Chart(most_liked_df).mark_bar().encode(
        x=alt.X('index', sort=None),
        y='likes',).properties(height=400),use_container_width=True)

# Show most liked posts images
path = [f'img/image{i}.jpg' for i in most_liked_df['index'][:x]]
from PIL import Image
cols = st.columns(len(path))
for i,col in enumerate(cols):
    with col:

        image = Image.open(path[i])
        st.image(image, caption=f'#{i+1} most liked image')



left,right = st.columns(2)
with left :
    # Most liked keyword
    most_liked_kw_df = df_key_word[['key_words','likes']]

    most_liked_kw_df = most_liked_kw_df.sort_values(by="likes",ascending=False)
    most_liked_kw_df = most_liked_kw_df[:n2]
    st.write('Most liked key words')
    st.altair_chart(alt.Chart(most_liked_kw_df).mark_bar().encode(
        x=alt.X('key_words', sort=None),
        y='likes',).properties(height=400),use_container_width=True)


# Most liked pondered keyword
most_liked_kw_df = df_key_word[['key_words','avg_likes']]

most_liked_kw_df = most_liked_kw_df.sort_values(by="avg_likes",ascending=False)
most_liked_kw_df = most_liked_kw_df[:n3]
with right :
    st.write('Most Average Liked Key Words')
    st.altair_chart(alt.Chart(most_liked_kw_df).mark_bar().encode(
        x=alt.X('key_words', sort=None),
        y='avg_likes',).properties(height=400),use_container_width=True)


## show knn images
# image = Image.open('knn_images.png')
# st.image(image, caption=f'Image Space Analysis')

df_knn = pd.read_csv('knn_images.csv')

fig, ax = plt.subplots()

for x,y,path,color in zip(list(df_knn['rawImages']),list(df_knn['features']),list(df_knn['filenames']),list(df_knn['norm_likes'])):

    y = y*10000
    #print(x,y)
    image = plt.imread(path)
    image_height, image_width = image.shape[:2]

    ax.imshow(image,  extent=[x,x+15*color, y,y+15*color])
    # Create a scatter plot using the x and y coordinates
    # Plot the x and y data as points
    ax.scatter(x, y, marker=",",color='white',alpha=0)



ax.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
ax.yaxis.label.set_color('white')          #setting up Y-axis label color to blue

ax.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
ax.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black

ax.spines['left'].set_color('white')        # setting up Y-axis tick color to red
ax.spines['top'].set_color('white')
st.write('Image Space Analysis')
fig.set_facecolor('#00172b')
st.pyplot(fig)
### hide elements
hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)
