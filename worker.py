# -*- coding: utf-8 -*-
import yaml
import argparse
import threading
from monitor import Monitor


if __name__ == '__main__':

	with open("config.yml", 'r') as f:
		config = yaml.load(f)

	parser = argparse.ArgumentParser()
	parser.add_argument('--city', metavar='city', type=str, help='city')
	args = parser.parse_args()

	city_data = config['data']
	city_data = [item for item in city_data if item['city'] == args.city][0]

	paris = Monitor(city_data)

	paris.init_posts()

	def callback():
		threading.Timer(60 * city_data['frequency'], callback).start()
		paris.monitor_change()

	callback()
