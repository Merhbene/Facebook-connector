

import json
import argparse
from facebook_scraper import get_posts

import pymongo
from pymongo import MongoClient


"""
Scrape post data from facebook page and store it in a mongoDB database

Usage : python fb_scraper_mongoDB.py --n  PageNames --email YourEmail --pw  YourPassword
Page name example (fb12.json): "dorrazarrouk"
Script runs on Python 3
@author: Oumaima Merhbene

"""

class FacebookScraper():
    def __init__(self,usernames,no_of_posts,email,password):
        self.no_of_posts = no_of_posts
        self.usernames = usernames
        self.email = email
        self.password = password

    def scrape_posts(self):
        # List to store all the data
        allData = [] 
        #Looping over all the usernames one by one
        for username in self.usernames:
            # Counter to stop when limit reached
            counter = 0
            # Get posts
            for post in get_posts(username,
                                  credentials=(self.email,self.password),
                                  options={
                                   "posts_per_page": 100,
                                   "comments":True,
                                  },
                                  pages=1000):
                
                # Break when limit reaches and continue with next username
                if counter >= self.no_of_posts: break
                # appending data scraped to the list
                allData.append(
                {
                    'post_text':   post['post_text'],
                    'comments' :   post['comments'],
                    'image_url':   post['image'],
                    'comments_full':  post['comments_full'],
                    'username':    username
                }
                )
                # incrementing the counter to get next data
                counter += 1

        return allData 



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument( "--n", help='user name or page name', required=True)
    parser.add_argument( "--email", help='your-email',required=True)
    parser.add_argument( "--pw", help='your-password',required=True)


    args = parser.parse_args()

    fb = FacebookScraper([args.n], 5, args.email, args.pw)
    data = fb.scrape_posts()

    # store data it in a mongoDB database
    cluster = MongoClient("mongodb+srv://oumaima:tM9grleQTebfFGqg@cluster0.sni7jaw.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["fb_data"]
    collection = db['fb_data']

    collection.insert_many(data)

