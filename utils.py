# -*- coding: utf-8 -*-
import os
import re 
import datetime
import yaml
import logging
from selenium import webdriver
import requests
from pymongo import MongoClient

# TODO
# https://intoli.com/blog/making-chrome-headless-undetectable/

# BROWSER = 'chrome'
# open browser and type in console: window.navigator.userAgent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"


def configure_logger(logger_name):
	# see https://docs.python.org/2/library/logging.html
	FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
	logging.basicConfig(format=FORMAT)
	logger = logging.getLogger(logger_name)
	# lowest level to be displayed
	logger.setLevel(logging.DEBUG)   

	return logger


logger = configure_logger('utils')


def get_config():
	with open("config.yml", 'r') as f:
		config = yaml.load(f)
	return config['data']
	

def get_db():
	client = MongoClient('mongodb://mongodb:27017/')
	db = client.house
	return db


def init_driver(browser='firefox', debug=False):

	assert browser in ['firefox', 'chrome']

	if browser == 'firefox':
		from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
		firefox_binary = FirefoxBinary(firefox_path="/Applications/Firefox.app/Contents/MacOS/firefox-bin", log_file=None)
		driver = webdriver.Firefox(firefox_binary=firefox_binary)
	
	elif browser == 'chrome':
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--window-size=1420,1080')
		chrome_options.add_argument('--headless')
		# chrome_options.add_argument("--start-maximized")
		# chrome_options.add_argument("--disable-notifications")
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument("--incognito")
		chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'fr'})
		# chrome_options.add_argument('--accept-language="en-US,en;q=0.8"')  
		chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
		driver = webdriver.Chrome(chrome_options=chrome_options)

	def whatismybrowser(driver):
		from bs4 import BeautifulSoup
		# print('[INFO] Info about the browser:')
		# driver.get("https://www.whatismybrowser.com")
		# html_source = driver.page_source
		# soup = BeautifulSoup(html_source, 'html.parser')
		# res = soup.findAll("div", {"class": "readout content"})
		# for r in res:
		# 	print(r)

		# print('[INFO] Info about the headers:')
		# driver.get("https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending")
		driver.get("https://httpbin.org/headers")
		html_source = driver.page_source
		# soup = BeautifulSoup(html_source, 'html.parser')
		# res = soup.findAll("div", {"class": "content"})
		# print(res)
		# print(html_source)
		logger.info('Info about the headers: %s', html_source)

		# print('[INFO] Info about the cookies:')
		# driver.get("https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending")
		driver.get("https://httpbin.org/cookies")
		html_source = driver.page_source
		# soup = BeautifulSoup(html_source, 'html.parser')
		# res = soup.findAll("div", {"class": "content"})
		# print(res)
		# print(html_source)
		logger.info('Info about the headers: %s', html_source)

	if (browser == 'chrome') and not debug:
		from inject import inject_js_with_driver
		inject_js_with_driver(driver)
		whatismybrowser(driver)

		r = driver.execute_script('return window.navigator.languages')
		print(r)

	return driver


# TODO : refactor !!
search_data = get_config()
searches = [item['city'] for item in search_data]
search_data = {searches[i]: [item for item in search_data if item['city'] == searches[i]][0] for i in range(len(searches))}
BROWSER = search_data['paris']['browser']

driver = init_driver(browser=BROWSER)


def get_page_source_selenium(url):
	driver.get(url)

	# TEST
	# https://selenium-python.readthedocs.io/waits.html
	# from selenium.webdriver.common.by import By
	# from selenium.webdriver.support.ui import WebDriverWait
	# from selenium.webdriver.support import expected_conditions as EC
	# wait 5 sec
	# print('[INFO] webdriver waiting for 10 sec')
	# element = WebDriverWait(driver, 10).until(
 	#        EC.presence_of_element_located((By.CLASS_NAME, "c-header-module-opener-text c-ep-opener-text"))
 	#    )

 	# DEBUG
	# print('[INFO] cartouche in html source (seloger): ', 'cartouche' in driver.page_source)

	return driver.page_source


def browse(urls, city):
	db = get_db()

	if BROWSER == 'firefox':
		for url in urls:
			os.system("open {}".format(url))

	elif BROWSER == 'chrome':
		for url in urls:
			item = {'url': url, 'city': city}
			db.urls.insert_one(item)
			logger.info('Inserted: %s', item)
			# print('[INFO] Inserted: ' + str(item))


def insert_one_to_mongo(collection, item):
	db = get_db()
	db[collection].insert_one(item)


def insert_to_mongo(collection, df):
	for index, row in df.iterrows():
		insert_one_to_mongo(collection, row.to_dict())


def save_last_check(city, site):
	item = {'date': datetime.datetime.now(),
			'city': city,
			'site': site}
	insert_one_to_mongo(collection='last_check', item=item)


def load_config_to_mongo():
	db = get_db()
	db.config.drop()
	searches = get_config()

	for item in searches:
		insert_one_to_mongo('config', item)


def keep_only_numeric(val):
	return re.sub("[^0-9\,]", "", val).replace(',', '.')
