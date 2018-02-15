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
captions = []  # list of captions for images


def get_images():
    global post_ids, captions
    count = 0
    # get 10 images from subreddit
    for submission in reddit.subreddit('NatureIsFuckingLit').hot():
        if count < 10:
            if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
                if str(submission.id) not in post_ids:
                    img_url = submission.url
                    _, extension = os.path.splitext(img_url)
                    if extension in ['.jpg', '.gif', '.jpeg', '.png']:
                        urllib.urlretrieve(
                            img_url, 'images/%i%s' % (count, extension))
                        count += 1
                        captions.append(submission.title)
                        post_ids.append(str(submission.id))
        else:
            break
    send_tweet()


def send_tweet():
    global post_ids, captions
    index = 0
    for x in captions:
        image = str(os.listdir("images")[index])
        api.update_with_media("images/" + image, captions[index])
        index += 1
        sleep(1440)  # tweet every 4 hours
    captions = []
    get_images()

if __name__ == '__main__':
    get_images()
