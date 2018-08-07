# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time, datetime
import os
import re 
import subprocess
import pandas as pd

from config import URLS, HEADERS, RATIO_MAX

def keep_only_numeric(val):
	return re.sub("[^0-9\,]", "", val).replace(',', '.')


def parse_seloger(soup, city):
	#posts = [post.find("a", {"class": "c-pa-link link_AB"}).attrs['href'] 
	# 		for post in soup.findAll("div", {"class": "c-pa-list c-pa-sl cartouche "})]

	posts = []
	prices = []
	surfaces = []

	for post in soup.findAll("div", {"class": "c-pa-list c-pa-sl cartouche "}):

		link = post.find("a", {"class": "c-pa-link link_AB"}).attrs['href'] 
		surface = post.find("div", {"class": "c-pa-criterion"})
		surface = surface.find_all("em")[1]
		price = post.find("div", {"class": "c-pa-price"})
		price = price.find("span", {"class": "c-pa-cprice"})

		if price:
			price = price.string
			price = keep_only_numeric(price)
			prices.append(price)
		if surface:
			surface = surface.string.split(u'm²')[0]
			surface = keep_only_numeric(surface)
			surfaces.append(surface)
		if price and surface:
			ratio = float(price) / float(surface)
			if ratio <= RATIO_MAX[city]:
				posts.append(link)

	return posts


def parse_pap(soup, city):
	url_pap = 'https://www.pap.fr'
	#posts = [url_pap + post.attrs['href'] for post in soup.findAll("a", {"class": "item-title"})]

	posts = []
	prices = []
	surfaces = []

	for post in soup.findAll("a", {"class": "item-title"}):

		link = url_pap + post.attrs['href']
		price = post.find("span", {"class": "item-price"})
		surface = post.find("span", {"class": "h1"})

		if price:
			price = price.strong.string
			price = keep_only_numeric(price)
			prices.append(price)
		if surface:
			surface = surface.string.split(u'm²')[0]
			surface = keep_only_numeric(surface)
			surfaces.append(surface)
		if price and surface:
			ratio = float(price) / float(surface)
			if ratio <= RATIO_MAX[city]:
				posts.append(link)

	url_to_discard = ['https://www.pap.fr//vendeur/estimation-gratuite',
					  'https://www.pap.fr//vendeur/bilan-projet-vente',
					  'https://www.pap.fr/annonceur/passer?produit=vente&itm_source=liste-annonces&itm_campaign=liste-annonces-pa-vente']
	#posts = [posts.remove(url_to_d) for url_to_d in url_to_discard if url_to_d in posts]	
	for url_to_d in url_to_discard:
		if url_to_d in posts:
			posts.remove(url_to_d)

	return posts


def parse_leboncoin(soup, city):
	url_leboncoin = 'https://www.leboncoin.fr'
	posts = [url_leboncoin + post.attrs['href']
			for post in soup.findAll("a", {"class": "clearfix trackable"})]

	return posts


def get_posts(site, city):
	response = requests.get(URLS[city][site], headers=HEADERS, allow_redirects=False)

	if not response.ok:
		print 'Could not connect to site:', site, ' - Error', response

	soup = BeautifulSoup(response.text, "html5lib")

	if site == 'seloger':
		posts = parse_seloger(soup, city)
	
	if site == 'pap':
		posts = parse_pap(soup, city)

	if site == 'leboncoin':
		posts = parse_leboncoin(soup, city)

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


def monitor_change(posts_old, site, city):
		posts = get_posts(site, city)
		
		new_posts = posts - posts_old
		if new_posts:
			browse(list(new_posts)) 
		
		posts_old = posts
		
		print len(new_posts), 'new post(s) on', site, city, '- last check at', datetime.datetime.now()
		if new_posts:
			print new_posts

		return posts_old


def save_all_to_cache(posts_old_seloger, posts_old_pap, posts_old_leboncoin, city):
	store = pd.HDFStore('cache_seloger.h5') 
	a = pd.DataFrame({'post': list(posts_old_seloger)}).assign(site='seloger')
	b = pd.DataFrame({'post': list(posts_old_pap)}).assign(site='pap')
	c = pd.DataFrame({'post': list(posts_old_leboncoin)}).assign(site='leboncoin')
	store['cache'] = pd.concat([a,b,c], 0).assign(city=city)
	store.close()
