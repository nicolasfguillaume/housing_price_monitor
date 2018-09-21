# -*- coding: utf-8 -*-
import yaml
import time
from monitor import Monitor

if __name__ == '__main__':

	with open("config.yml", 'r') as f:
		config = yaml.load(f)

	# for city_data in config['data']: # TODO
	city_data = config['data']
	paris = Monitor(city_data[0])
	idf = Monitor(city_data[1])

	paris.init_posts()
	idf.init_posts()
	
	while True:	
		paris.monitor_change()
		idf.monitor_change() 
		time.sleep(60 * 15) # 15 min
