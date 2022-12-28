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
n2 = st.sidebar.slider('Number of key words',min_value=4,max_value=18,value=8)  # 👈 this is a widget
n3 = st.sidebar.slider('Number of key words (avg)',min_value=4,max_value=28,value=8)  # 👈 this is a widget
# x = st.sidebar.slider('Number of key words shown',min_value=4,max_value=28,value=8)  # 👈 this is a widget
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

# Show most liked posts images
path = [f'img/image{i}' for i in df['index'][:4]]

# Most liked pondered keyword
most_liked_kw_df = df_key_word[['key_words','avg_likes']]

most_liked_kw_df = most_liked_kw_df.sort_values(by="avg_likes",ascending=False)
most_liked_kw_df = most_liked_kw_df[:n3]
with right :
    st.write('Most Average Liked Key Words')
    st.altair_chart(alt.Chart(most_liked_kw_df).mark_bar().encode(
        x=alt.X('key_words', sort=None),
        y='avg_likes',).properties(height=400),use_container_width=True)

#
# # Pie chart for work
# left,right = st.columns(2)
# fig1, ax1 = plt.subplots()
# fig1.set_facecolor('#00172b')
# patches,texts,autotext= ax1.pie(work_df['counts'], labels=work_df['work_type'], autopct='%1.1f%%',
#         shadow=False, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# for text in texts:
#     text.set_color('white')
# with left:
#     st.write('Types of work')
#     st.pyplot(fig1)
#
# # Pie chart for schedule type
# schedule_type_df['schedual'] = schedule_type_df.index
# fig1, ax1 = plt.subplots()
# fig1.set_facecolor('#00172b')
# patches,texts,autotexts= ax1.pie(schedule_type_df['counts'], labels=schedule_type_df['schedual'],autopct='%1.1f%%',
#         shadow=False, startangle=90)
# for text in texts:
#     text.set_color('white')
#
#
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#
# # Move a label
# try:
#     texts[1]._x +=0.05
#     texts[1]._y -= 0.05
#     texts[3]._x -=0.05
#     texts[3]._y += 0.05
#     autotext[1]._y -=0.1
#     autotext[3]._y += 0.1
# except:
#     pass
# plt.tight_layout()
# with right:
#     st.write('Types of contracts')
#     st.pyplot(fig1)



### hide elements
hide_st_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)
