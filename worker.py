# -*- coding: utf-8 -*-
import yaml
import threading

from monitor import Monitor
from utils import get_db, get_config

if __name__ == '__main__':

	search_data = get_config()
	searches = [item['city'] for item in search_data]
	print('[INFO] Searches: ', searches)

	search_data = {searches[i]: [item for item in search_data if item['city'] == searches[i]][0] for i in range(len(searches))}
	search = {idx: Monitor(search_data[idx]) for idx in searches}

	def callback():
		# threading.Timer(60 * search_data['paris']['frequency'], callback).start()
		import random
		wait_time = random.randint(4,7) # between 4 and 6 min
		threading.Timer(60 * wait_time, callback).start()

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
