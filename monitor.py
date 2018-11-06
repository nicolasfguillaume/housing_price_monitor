# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd

from utils import parse_seloger, parse_pap, parse_leboncoin, get_page_source_selenium, browse

HEADERS = {'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106  Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		  }

class Monitor(object):

	def __init__(self, ctx):
		self.ctx = ctx
		self.city = ctx['city']
		self.frequency = ctx['frequency']
		self.ratio_max = ctx['ratio_max']
		self.urls = ctx['urls']
		self.posts = {}


	def init_posts(self):
		for site in self.urls:
			print('[INFO] Monitoring: ' + self.urls[site])
			self.posts[site] = set(self.check_posts(site))
			self.save_to_cache(list(self.posts[site]), site)


	def get_posts(self, site):		
		return self.posts[site]


	def get_page_source(self, site):
		# marche si la page ne contient pas de JS
		try:
			response = requests.get(self.urls[site], headers=HEADERS, allow_redirects=True)
			if not response.ok:
				print('[ERROR] Could not connect to site: ' + site, ' - ' + self.response)
			return response.text
		except:
			print('[ERROR] Could not connect to site: ' + site)
			return None


	def check_posts(self, site):
		if site == 'seloger':
			html_source = get_page_source_selenium(self.urls[site])
		else:
			html_source = self.get_page_source(site)

		soup = BeautifulSoup(html_source, 'html.parser')
		# soup = BeautifulSoup(html_source, 'lxml')
		# soup = BeautifulSoup(html_source, 'html5lib')

		if site == 'seloger':
			posts = parse_seloger(soup, self.city, self.ratio_max)
		if site == 'pap':
			posts = parse_pap(soup, self.city, self.ratio_max)
		if site == 'leboncoin':
			posts = parse_leboncoin(soup, self.city, self.ratio_max)

		if not posts:
			print('[ERROR] Could not parse site: ' + site)

		# compare seulement avec les 10 derniers posts
		if len(posts) > 10:
			posts = posts[0:10]

		self.save_to_cache(posts, site)

		return posts


	def save_to_cache(self, posts, site):
		store = pd.HDFStore('cache.h5') 
		df = pd.DataFrame({'post': list(posts)}).assign(site=site).assign(city=self.city)
		if 'cache' not in store:
			store['cache'] = df
		else:
			store['cache'] = pd.concat([store['cache'], df], axis=0).drop_duplicates()
		store.close()


	def get_from_cache(self, site):
		store = pd.HDFStore('cache.h5') 
		df = store['cache']
		store.close()
		return df.loc[(df.site == site) & (df.city == self.city), 'post'].tolist()


	def monitor_change(self):
		for site in self.urls:
			posts_old = set(self.get_from_cache(site))
			posts = set(self.check_posts(site))
			new_posts = posts - posts_old
			print('[INFO] ' + str(len(new_posts)) + ' new post(s) on ' + site + ' for ' + self.city + ' (' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ')')

			if new_posts:
				browse(list(new_posts)) 
