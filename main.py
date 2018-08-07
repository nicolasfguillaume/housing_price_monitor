# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time, datetime
import os, sys
import subprocess
import pandas as pd

from config import URLS, HEADERS, FREQUENCY
from utils import get_posts, monitor_change, save_all_to_cache

if __name__ == '__main__':

	if len(sys.argv) > 1:
		city = sys.argv[1]
	else:
		print 'argument is missing: city'
		raise

	print 'Monitoring:', URLS[city]['seloger']
	posts_old_seloger = get_posts(site='seloger', city=city)
	print 'Monitoring:', URLS[city]['pap']
	posts_old_pap = get_posts(site='pap', city=city)
	print 'Monitoring:', URLS[city]['leboncoin']
	posts_old_leboncoin = get_posts(site='leboncoin', city=city)

	save_all_to_cache(posts_old_seloger, posts_old_pap, posts_old_leboncoin, city)

	while True:

		store = pd.HDFStore('cache_seloger.h5') 
		df = store['cache']
		store.close()

		try:
			site = 'seloger'
			posts_old_seloger = set(df.loc[df.site == site, 'post'].tolist())
			posts_old_seloger = monitor_change(posts_old_seloger, site=site, city=city)
		except:
			print 'An error occured while checking', site, city

		try:
			site = 'pap'
			posts_old_pap = set(df.loc[df.site == site, 'post'].tolist())
			posts_old_pap = monitor_change(posts_old_pap, site=site, city=city)
		except:
			print 'An error occured while checking', site, city

		try:
			site = 'leboncoin'
			posts_old_leboncoin = set(df.loc[df.site == site, 'post'].tolist())
			posts_old_leboncoin = monitor_change(posts_old_leboncoin, site=site, city=city)
		except:
			print 'An error occured while checking', site, city

		save_all_to_cache(posts_old_seloger, posts_old_pap, posts_old_leboncoin, city)
		
		time.sleep(60 * FREQUENCY[city])