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

	search_data = config['data']
	searches = [item['city'] for item in search_data]
	print('[INFO] Searches: ', searches)

	# search_0_data = [item for item in search_data if item['city'] == searches[0]][0]
	# search_1_data = [item for item in search_data if item['city'] == searches[1]][0]
	search_data = {searches[i]: [item for item in search_data if item['city'] == searches[i]][0] for i in range(len(searches))}

	# search_0 = Monitor(search_data['paris'])
	# search_0 = Monitor(search_0_data)
	# search_1 = Monitor(search_data['idf'])
	# search_1 = Monitor(search_1_data)
	search = {idx: Monitor(search_data[idx]) for idx in searches}

	def callback():
		threading.Timer(60 * search_data['paris']['frequency'], callback).start()
		
		# search_0.monitor_change()
		# search_1.monitor_change()
		for idx in searches:
			search[idx].monitor_change()

	callback()


# TEST asyncio
# https://medium.freecodecamp.org/a-guide-to-asynchronous-programming-in-python-with-asyncio-232e2afa44f6

# import asyncio  

# async def custom_sleep():  
#     print('SLEEP {}\n'.format(datetime.now()))
#     await asyncio.sleep(1)

# async def factorial(name, number):  
#     f = 1
#     for i in range(2, number+1):
#         print('Task {}: Compute factorial({})'.format(name, i))
#         await custom_sleep()
#         f *= i
#     print('Task {}: factorial({}) is {}\n'.format(name, number, f))

# loop = asyncio.get_event_loop()

# tasks = [  
#     asyncio.ensure_future(factorial("A", 3)),
#     asyncio.ensure_future(factorial("B", 4)),
# ]

# loop.run_until_complete(asyncio.wait(tasks))  

# loop.close()
