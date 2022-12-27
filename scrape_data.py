import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile
import csv
import time
import pandas as pd


class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()

    def download_users_profile_picture(self,username):
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periods(self,username):
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        SINCE = datetime(2021, 8, 28)
        UNTIL = datetime(2021, 9, 30)

        for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
            self.L.download_post(post, username)

    def download_hastag_posts(self, hashtag):
        for post in instaloader.Hashtag.from_name(self.L.context, hashtag).get_posts():
            self.L.download_post(post, target='#'+hashtag)

    def get_users_followers(self,user_name):
        '''Note: login required to get a profile's followers.'''
        self.L.login(input("input your username: "), input("input your password: ") )
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("follower_names.txt","a+")
        for followee in profile.get_followers():
            username = followee.username
            file.write(username + "\n")
            print(username)

    def get_users_followings(self,user_name):
        '''Note: login required to get a profile's followings.'''
        self.L.login(input("input your username: "), input("input your password: ") )
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("following_names.txt","a+")
        for followee in profile.get_followees():
            username = followee.username
            file.write(username + "\n")
            print(username)

    def get_post_comments(self,username):
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        for post in posts:
            for comment in post.get_comments():
                print("comment.id  : "+str(comment.id))
                print("comment.owner.username  : "+comment.owner.username)
                print("comment.text  : "+comment.text)
                print("comment.created_at_utc  : "+str(comment.created_at_utc))
                print("************************************************")

    def get_post_info_csv(self,username):
        #with open(username+'.csv', 'w', newline='', encoding='utf-8') as file:
        #writer = csv.writer(file)
        try:
            df = pd.read_csv('gresunstudio.csv')
            downloaded_media = list(df['posturl'])
        except:
            df = pd.DataFrame()
            downloaded_media = []
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        len_df = df.shape[0]

        for post in posts:


            # print("post date: "+str(post.date))
            # print("post profile: "+post.profile)
            # print("post caption: "+post.caption)
            # print("post location: "+str(post.location))
            try:
                posturl = "https://www.instagram.com/p/"+post.shortcode

                if not posturl in downloaded_media:
                    print("post url: "+posturl)
                    row = pd.DataFrame({'media':[post.mediaid],'profile':[post.profile],'caption':[post.caption],'date':[post.date],'location':[post.location],'posturl':[posturl],'typename':[post.typename],'mediacount':[post.mediacount],'caption_hashtags':[post.caption_hashtags],'caption_mentions':[post.caption_mentions],'tagged_users':[post.tagged_users],'likes':[post.likes],'comments': [post.comments],  'title': [post.title], 'img_url':  [post.url] })
                    df = pd.concat([df,row],ignore_index=True)
                    df.to_csv('gresunstudio.csv',index=False)
            except:
                pass


            # for comment in post.get_comments():
            #     writer.writerow(["comment",comment.id, comment.owner.username,comment.text,comment.created_at_utc])
            #     print("comment username: "+comment.owner.username)
            #     print("comment text: "+comment.text)
            #     print("comment date : "+str(comment.created_at_utc))
            #print("\n")



if __name__=="__main__":
    cls = GetInstagramProfile()

    cls.get_post_info_csv("gresunstudio")
