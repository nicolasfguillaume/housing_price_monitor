# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time, datetime
import os
import subprocess
import pandas as pd

from config import URLS, HEADERS
from utils import get_posts, monitor_change, save_all_to_cache

if __name__ == '__main__':

	print 'Monitoring:', URLS['seloger']
	posts_old_seloger = get_posts(site='seloger')
	print 'Monitoring:', URLS['pap']
	posts_old_pap = get_posts(site='pap')
	print 'Monitoring:', URLS['leboncoin']
	posts_old_leboncoin = get_posts(site='leboncoin')

	store = pd.HDFStore('cache_seloger.h5') 
	save_all_to_cache(store, posts_old_seloger, posts_old_pap, posts_old_leboncoin)

	while True:

		store = pd.HDFStore('cache_seloger.h5') 
		df = store['cache']

		try:
			site = 'seloger'
			posts_old_seloger = set(df.loc[df.site == site, 'post'].tolist())
			posts_old_seloger = monitor_change(posts_old_seloger, site=site)
		except:
			print 'An error occured while checking', site

		try:
			site = 'pap'
			posts_old_pap = set(df.loc[df.site == site, 'post'].tolist())
			posts_old_pap = monitor_change(posts_old_pap, site=site)
		except:
			print 'An error occured while checking', site

		try:
			site = 'leboncoin'
			posts_old_leboncoin = set(df.loc[df.site == site, 'post'].tolist())
			posts_old_leboncoin = monitor_change(posts_old_leboncoin, site=site)
		except:
			print 'An error occured while checking', site

		save_all_to_cache(store, posts_old_seloger, posts_old_pap, posts_old_leboncoin)
		store.close()

		time.sleep(60*5)