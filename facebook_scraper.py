"""

Usage : python facebook_scraper.py --n  PageNames --email YourEmail --pw  YourPassword
Page name example (fb12.json): "dorrazarrouk"
Script runs on Python 3
@author: Oumaima Merhbene

"""
import json
import argparse
from facebook_scraper import get_posts


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
        # Returning the all scraped data in json file
        for post in allData:
            with open('fb12.json', 'a', encoding='utf-8') as f:
                json.dump(post, f, ensure_ascii=False, default=str)
                f.write("\n")
        return 



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument( "--n", help='user name or page name', required=True)
    parser.add_argument( "--email", help='your-email',required=True)
    parser.add_argument( "--pw", help='your-password',required=True)


    args = parser.parse_args()

    fb = FacebookScraper([args.n], 5, args.email, args.pw)
    fb.scrape_posts()
