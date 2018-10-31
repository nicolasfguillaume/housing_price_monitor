# -*- coding: utf-8 -*-
import os
import re 
from selenium import webdriver
import requests

BROWSER = 'chrome'


def init_driver(browser='firefox'):

	if browser == 'firefox':
		from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
		firefox_binary = FirefoxBinary(firefox_path="/Applications/Firefox.app/Contents/MacOS/firefox-bin", log_file=None)
		driver = webdriver.Firefox(firefox_binary=firefox_binary)
	
	elif browser == 'chrome':
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--window-size=1420,1080')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(chrome_options=chrome_options)

	return driver


driver = init_driver(browser=BROWSER)


def get_page_source_selenium(url):
	driver.get(url)
	html_source = driver.page_source
	return html_source


def browse(urls):
	if BROWSER == 'firefox':
		for url in urls:
			os.system("open {}".format(url))

	elif BROWSER == 'chrome':
		for url in urls:
			with open('to_open_in_browser.csv', 'a') as f:
				f.write(url + "\n")


def keep_only_numeric(val):
	return re.sub("[^0-9\,]", "", val).replace(',', '.')


def parse_seloger(soup, city, ratio_max):
	posts = []
	prices = []
	surfaces = []

	# print soup.prettify() # DEBUG

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
	url_pap = 'https://www.pap.fr'

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
			if ratio <= ratio_max:
				posts.append(link)

	url_to_discard = ['https://www.pap.fr//vendeur/estimation-gratuite',
					  'https://www.pap.fr//vendeur/bilan-projet-vente',
					  'https://www.pap.fr/annonceur/passer?produit=vente&itm_source=liste-annonces&itm_campaign=liste-annonces-pa-vente']

	for url_to_d in url_to_discard:
		if url_to_d in posts:
			posts.remove(url_to_d)

	return posts


def parse_leboncoin(soup, city, ratio_max):
	url_leboncoin = 'https://www.leboncoin.fr'

	posts = [url_leboncoin + post.attrs['href']
			for post in soup.findAll("a", {"class": "clearfix trackable"})]

	return posts
