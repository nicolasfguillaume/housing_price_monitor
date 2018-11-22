# -*- coding: utf-8 -*-
from utils import keep_only_numeric

def parse_seloger(soup, city, ratio_max):
	posts = []
	prices = []
	surfaces = []

	# DEBUG
	# debug = soup.prettify()[53000:57000]
	# print(debug)
	# print('cartouche in debug:')
	# print('cartouche' in debug)
	# print('persoModuleContent in debug:')
	# print('persoModuleContent' in debug)

	for post in soup.findAll("div", {"class": "c-pa-list c-pa-sl cartouche "}):

		link = post.find("a", {"class": "c-pa-link link_AB"}).attrs['href'] 
		surface = post.find("div", {"class": "c-pa-criterion"})
		surface = surface.find_all("em")
		if surface:
			surface = surface[1]
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
			if ratio <= ratio_max:
				posts.append(link)

	return posts


def parse_pap(soup, city, ratio_max):
	"""pour annonces de ventes immo et locations""" 
	url_pap = 'https://www.pap.fr'

	posts = []
	prices = []
	surfaces = []

	for post in soup.findAll("a", {"class": "item-title"}):

		link = url_pap + post.attrs['href']

		# TODO refactor
		if 'adtech.de/adlink' in link:
			continue
		if 'adtech.advertising.com/adlink' in link:
			continue
		if 'vendeur/estimation-gratuite' in link:
			continue
		if 'immoneuf.com/programme' in link:
			continue

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

		if ratio_max:
			if ratio <= ratio_max:
				posts.append(link)
		else:
			posts.append(link)

	url_to_discard = ['https://www.pap.fr//vendeur/estimation-gratuite',
					  'https://www.pap.fr//vendeur/bilan-projet-vente',
					  'https://www.pap.fr/annonceur/passer?produit=vente&itm_source=liste-annonces&itm_campaign=liste-annonces-pa-vente']

	for url_to_d in url_to_discard:
		if url_to_d in posts:
			posts.remove(url_to_d)

	return posts


def parse_leboncoin(soup, city, ratio_max):
	"""pour annonces de ventes immo et locations""" 
	url_leboncoin = 'https://www.leboncoin.fr'

	posts = [url_leboncoin + post.attrs['href']
			for post in soup.findAll("a", {"class": "clearfix trackable"})]

	return posts