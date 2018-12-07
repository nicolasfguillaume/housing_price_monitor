# -*- coding: utf-8 -*-
import yaml
import threading
import random
import asyncio
import time

from monitor import Monitor
from utils import get_db, get_config, configure_logger

logger = configure_logger('worker')

# WORKS 3 dec 2018
# if __name__ == '__main__':

# 	search_data = get_config()
# 	searches = [item['city'] for item in search_data]
# 	print('[INFO] Searches: ', searches)

# 	search_data = {searches[i]: [item for item in search_data if item['city'] == searches[i]][0] for i in range(len(searches))}
# 	search = {idx: Monitor(search_data[idx]) for idx in searches}

# 	def callback():
# 		# threading.Timer(60 * search_data['paris']['frequency'], callback).start()
# 		wait_time = random.randint(4,7) # between 4 and 6 min
# 		threading.Timer(60 * wait_time, callback).start()

# 		for idx in searches:
# 			search[idx].monitor_change()

# 	callback()


# TEST: asyncio
# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
# An event loop basically waits for something to happen and then acts on the event.
# An event loop basically says “when event A happens, react with function B”.
# The async / await keywords can be considered an API to be used for asynchronous programming.
# Future objects are created with the intention that they will eventually be given a result some time in the future.
# See also: https://medium.freecodecamp.org/a-guide-to-asynchronous-programming-in-python-with-asyncio-232e2afa44f6

# define a coroutine
async def monitor_change_loop(search_idx):
	while True:
		search_idx.monitor_change()
		wait_time = random.randint(4, 7) * 60 # wait between 4 and 6 min
		logger.info('Waiting for: %s sec', wait_time)
		await asyncio.sleep(wait_time)


if __name__ == '__main__':

	search_data = get_config()
	searches = [item['city'] for item in search_data]
	logger.info('Searches: %s', searches)

	search_data = {searches[i]: [item for item in search_data if item['city'] == searches[i]][0] for i in range(len(searches))}
	search = {idx: Monitor(search_data[idx]) for idx in searches}

	loop = asyncio.get_event_loop()
	try:
		for idx in searches:
			# enqueue coroutines onto the loop
			asyncio.ensure_future(monitor_change_loop(search[idx]))
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	finally:
		logger.info('Closing Loop')
		loop.close()
