# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time, datetime
import os
import subprocess
import pandas as pd

from config import URLS, HEADERS

def parse_seloger(soup):
	posts = [post.find("a", {"class": "c-pa-link link_AB"}).attrs['href'] 
	 		for post in soup.findAll("div", {"class": "c-pa-list c-pa-sl cartouche "})]

	return posts


def parse_pap(soup):
	url_pap = 'https://www.pap.fr'
	#posts = [url_pap + post.attrs['href'] for post in soup.findAll("a", {"class": "item-title"})]

	posts = []
	prices = []
	surfaces = []

	for post in soup.findAll("a", {"class": "item-title"}):
		price = post.find("span", {"class": "item-price"})
		if price:
			price = price.strong.string
			import re 
			price = re.sub("[^0-9]", "", price)
			prices.append(price)
		surface = post.find("span", {"class": "h1"})
		if surface:
			surface = surface.string.split(u'm²')[0]
			surface = re.sub("[^0-9]", "", surface)
			surfaces.append(surface)
		if price and surface:
			ratio = float(price) / float(surface)
			if ratio <= 10000.0:
				posts.append(url_pap + post.attrs['href'])

	url_to_discard = ['https://www.pap.fr//vendeur/estimation-gratuite',
					  'https://www.pap.fr//vendeur/bilan-projet-vente',
					  'https://www.pap.fr/annonceur/passer?produit=vente&itm_source=liste-annonces&itm_campaign=liste-annonces-pa-vente']
	#posts = [posts.remove(url_to_d) for url_to_d in url_to_discard if url_to_d in posts]	
	for url_to_d in url_to_discard:
		if url_to_d in posts:
			posts.remove(url_to_d)

	return posts


def parse_leboncoin(soup):
	url_leboncoin = 'https://www.leboncoin.fr'
	posts = [url_leboncoin + post.attrs['href']
			for post in soup.findAll("a", {"class": "clearfix trackable"})]

	return posts


def get_posts(site):
	response = requests.get(URLS[site], headers=HEADERS, allow_redirects=False)

	if not response.ok:
		print 'Could not connect to site:', site, ' - Error', response

	soup = BeautifulSoup(response.text, "html5lib")

	if site == 'seloger':
		posts = parse_seloger(soup)
	
	if site == 'pap':
		posts = parse_pap(soup)

	if site == 'leboncoin':
		posts = parse_leboncoin(soup)

	if not posts:
		print 'Could not parse site:', site

	# compare seulement avec les 10 derniers posts, pour eviter de faire reapparaitre des anciens posts
	# lorsque des posts recents sont supprimes
	if len(posts) > 10:
		return set(posts[0:10])
	else:
		return set(posts)


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


def save_all_to_cache(store, posts_old_seloger, posts_old_pap, posts_old_leboncoin):
		a = pd.DataFrame({'post': list(posts_old_seloger)}).assign(site='seloger')
		b = pd.DataFrame({'post': list(posts_old_pap)}).assign(site='pap')
		c = pd.DataFrame({'post': list(posts_old_leboncoin)}).assign(site='leboncoin')
		store['cache'] = pd.concat([a,b,c], 0)
