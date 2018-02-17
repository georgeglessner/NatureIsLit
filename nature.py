#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import tweepy
from time import sleep
from credentials import *
import praw
import requests
import urllib
import os

# connect to reddit
reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET,
                     password=PASSWORD,
                     user_agent=AGENT,
                     username=USERNAME)

# connect to twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# create images folder if one does not exits
if not os.path.exists('./images'):
    os.mkdir('./images')

post_ids = []  # keeps track of used posts
caption = ''  # caption for image
extension = ''


def get_images():
    global post_ids, caption
    count = 0
    ids = []

    with open('post_ids.txt') as f:
        ids = f.readlines()
    ids = [x.strip() for x in ids]

    # get 10 images from subreddit
    for submission in reddit.subreddit('NatureIsFuckingLit').hot():
        if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
            if str(submission.id) not in ids:
                id_num = open('post_ids.txt', 'a')
                id_num.write(str(submission.id + '\n'))
                id_num.close()
                img_url = submission.url
                _, extension = os.path.splitext(img_url)
                if extension == '.jpg':
                    urllib.urlretrieve(
                        img_url, 'images/image.jpg')
                    caption = submission.title
                    post_ids.append(str(submission.id))
                    break
                if extension == '.jpeg':
                    urllib.urlretrieve(
                        img_url, 'images/image.jpeg')
                    caption = submission.title
                    post_ids.append(str(submission.id))
                    break
                if extension == '.gif':
                    urllib.urlretrieve(
                        img_url, 'images/image.gif')
                    caption = submission.title
                    post_ids.append(str(submission.id))
                    break
                if extension == '.png':
                    urllib.urlretrieve(
                        img_url, 'images/image.png')
                    caption = submission.title
                    post_ids.append(str(submission.id))
                    break

    send_tweet(extension)


def send_tweet(extension):
    global post_ids, caption
    api.update_with_media("images/image" + extension, caption)
    print 'tweeting'
    sleep(10800)  # tweet every 3 hours
    captions = []
    get_images()


if __name__ == '__main__':
    get_images()
