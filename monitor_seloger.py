# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time, datetime
import os
import subprocess

URLS = {'seloger': "http://www.seloger.com/list.htm?types=1%2C2&projects=2&sort=d_dt_crea&natures=1%2C2%2C4&price=150000%2F175000&surface=15%2FNaN&places=%5B%7Bcp%3A75%7D%5D&qsVersion=1.0&engine-version=new",
		'pap': "https://www.pap.fr/annonce/vente-appartement-maison-paris-75-g439-jusqu-a-175000-euros-a-partir-de-15-m2",
		'leboncoin': "https://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/paris/?th=1&ps=6&pe=7"}

HEADERS = {'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
		  }

def get_posts(site):
	response = requests.get(URLS[site], headers=HEADERS, allow_redirects=False)
	soup = BeautifulSoup(response.text, "html5lib")

	if site == 'seloger':
		posts = [post.find("a", {"class": "link_AB"}).attrs['href'] 
			 for post in soup.findAll("div", {"class": "c-pa-list c-pa-sl cartouche "})]
	
	if site == 'pap':
		url_pap = 'https://www.pap.fr'
		posts = [url_pap + post.attrs['href'] for post in soup.findAll("a", {"class": "item-title"})]
		url_to_discard = ['https://www.pap.fr//vendeur/estimation-gratuite',
						  'https://www.pap.fr//vendeur/bilan-projet-vente']
		posts = [posts.remove(url_to_d) for url_to_d in url_to_discard if url_to_d in posts]			 

	if site == 'leboncoin':
		url_leboncoin = 'https://'
		posts = [url_leboncoin + post.attrs['href'][2:] 
		for post in soup.findAll("a", {"class": "list_item clearfix trackable"})]


	# compare seulement avec les 10 derniers posts, pour eviter de faire reapparaitre des anciens posts
	# lorsque des posts recents sont supprimes
	return set(posts[0:10])

def browse(urls):
	for url in urls:
		os.system("open {}".format(url))

def monitor_change(posts_old, site):

		posts = get_posts(site)
		
		new_posts = posts - posts_old
		if new_posts:
			# TODO calculer le eur/m2 et filtrer sur < 9000
			browse(list(new_posts)) 
		
		posts_old = posts
		
		print len(new_posts), 'new post(s) on', site,'- last check at', datetime.datetime.now()
		if new_posts:
			print new_posts

		return posts_old


if __name__ == '__main__':

	print 'Monitoring:', URLS['seloger']
	posts_old_seloger = get_posts(site='seloger')
	print 'Monitoring:', URLS['pap']
	posts_old_pap = get_posts(site='pap')
	print 'Monitoring:', URLS['leboncoin']
	posts_old_leboncoin = get_posts(site='leboncoin')

	# store = pd.HDFStore('cache_seloger.h5') 

	while True:

		try:
			posts_old_seloger = monitor_change(posts_old_seloger, site='seloger')
		except:
			print 'An error occured while checking seloger'

		try:
			posts_old_pap = monitor_change(posts_old_pap, site='pap')
		except:
			print 'An error occured while checking pap'

		try:
			posts_old_leboncoin = monitor_change(posts_old_leboncoin, site='leboncoin')
		except:
			print 'An error occured while checking leboncoin'

		time.sleep(60*5)