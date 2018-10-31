# -*- coding: utf-8 -*-
import yaml
import time
import argparse

from monitor import Monitor

# doc: python worker.py --city=paris

if __name__ == '__main__':

	with open("config.yml", 'r') as f:
		config = yaml.load(f)

	parser = argparse.ArgumentParser()
	# parser.add_argument('--city', metavar='city', type=unicode, help='city')  # 2.7
	parser.add_argument('--city', metavar='city', type=str, help='city')  # 3.6
	args = parser.parse_args()

	city_data = config['data']
	city_data = [item for item in city_data if item['city'] == args.city][0]
	paris = Monitor(city_data)

	# debug
	# url = 'test123'
	# import requests
	# r = requests.post('http://web:5000/api', json={"url": url})
	# # r = requests.get('http://web:5000/api')
	# print(repr(url) + repr(r.status_code))

	paris.init_posts()
	
	while True:	
		paris.monitor_change()
		time.sleep(60 * city_data['frequency'])
