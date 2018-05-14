# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time, datetime
import os
import subprocess

url = "http://www.seloger.com/list.htm?types=1%2C2&projects=2&sort=d_dt_crea&natures=1%2C2%2C4&price=150000%2F175000&surface=15%2FNaN&places=%5B%7Bcp%3A75%7D%5D&qsVersion=1.0&engine-version=new"

headers = {'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
          }

response = requests.get(url, headers=headers, allow_redirects=False)
soup = BeautifulSoup(response.text, "html5lib")

def update():
    return [post.find("a", {"class": "link_AB"}).attrs['href'] 
         for post in soup.findAll("div", {"class": "c-pa-list c-pa-sl cartouche "})]

def browse(urls):
    for url in urls:
        os.system("open {}".format(url))

if __name__ == '__main__':

	print 'Monitoring:', url

	posts_old = set(update())

	while True:
	    response = requests.get(url, headers=headers, allow_redirects=False)
	    soup = BeautifulSoup(response.text, "html5lib")
	    posts = update()
	    # compare seulement avec les 10 derniers posts, pour eviter de faire reapparaitre des anciens posts
	    # lorsque des posts recents sont supprimes
	    posts = set(posts[0:10])
	    
	    new_posts = posts - posts_old
	    if new_posts:
	        # TODO calculer le eur/m2 et filtrer sur < 9000
	        browse(list(new_posts)) 
	    
	    posts_old = posts
	    
	    print len(new_posts), 'new post(s) - last check at', datetime.datetime.now()
	    if new_posts:
	        print new_posts

	    time.sleep(60*5)