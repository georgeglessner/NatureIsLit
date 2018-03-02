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

caption = ''  # caption for image
extension = ''


def get_images():
    ''' Get posts/images from reddit '''

    global caption
    count = 0
    ids = []
    statuses = []

    # get 20 latest tweets on your timeline, add to list
    tweets = api.user_timeline(screen_name='nature_is_lit')
    for status in tweets:
        status = status.text.split('https', 1)
        status = status[0].strip()
        # lengthy statuses cut off, cannot compare accurately, get duplicates
        # do not add these statuses to list
        if len(status) > 100:
            pass
        else:
            statuses.append(status)
    # get submissions in subreddit
    for submission in reddit.subreddit('NatureIsFuckingLit').hot():
        if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
            # make sure you have not tweeted this post already
            if submission.title not in statuses:
                img_url = submission.url
                _, extension = os.path.splitext(img_url)
                if extension == '.jpg':
                    urllib.urlretrieve(
                        img_url, 'images/image.jpg')
                    file_size = os.stat('images/image.jpg')
                    if file_size.st_size > 3145728:
                        print 'file too big'
                    else:
                        caption = submission.title
                        break
                if extension == '.jpeg':
                    urllib.urlretrieve(
                        img_url, 'images/image.jpeg')
                    file_size = os.stat('images/image.jpeg')
                    if file_size.st_size > 3145728:
                        print 'file too big'
                    else:
                        caption = submission.title
                        break
                if extension == '.gif':
                    urllib.urlretrieve(
                        img_url, 'images/image.gif')
                    file_size = os.stat('images/image.gif')
                    if file_size.st_size > 3145728:
                        print 'file too big'
                    else:
                        caption = submission.title
                        break
                if extension == '.gifv':
                    img_url = submission.url.split('.gifv')
                    img_url = img_url[0] + '.gif'
                    urllib.urlretrieve(
                        img_url, 'images/image.gif')
                    file_size = os.stat('images/image.gif')
                    if file_size.st_size > 3145728:
                        print 'file too big'
                    else:
                        caption = submission.title
                        break
                if extension == '.png':
                    urllib.urlretrieve(
                        img_url, 'images/image.png')
                    file_size = os.stat('images/image.png')
                    if file_size.st_size > 3145728:
                        print 'file too big'
                    else:
                        caption = submission.title
                        break
            else:
                print 'Tweet already exists in timeline'

    send_tweet(extension)


def favorite_tweets():
    ''' Favorite tweets containing keyword "Nature is lit" '''

    results = api.search(q='"nature is lit"', lang="en")
    for result in results:
        if result.author._json['screen_name'] != 'Nature_Is_Lit':
            try:
                if not result.favorited:
                    api.create_favorite(result.id)
                    print 'Favorited a tweet by', result.author._json['screen_name']
            except tweepy.TweepError:
                print 'Tweet already favorited'


def send_tweet(extension):
    ''' Send Tweet '''

    global caption
    api.update_with_media("images/image" + extension, caption)
    print 'sending tweet'
    print 'searching for tweets to favorite'
    favorite_tweets()
    print 'sleeping 2 hours'
    sleep(7200)  # tweet every 2 hours
    get_images()


if __name__ == '__main__':
    get_images()
