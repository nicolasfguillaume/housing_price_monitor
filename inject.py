import os, datetime
from selenium import webdriver

from utils import configure_logger

logger = configure_logger('inject')

URL = "https://www.leboncoin.fr/recherche/?category=9&regions=12&departments=92&department_near=1&real_estate_type=1,2,5&price=75000-125000"

# https://intoli.com/blog/javascript-injection/

# The JavaScript that we want to inject.
# `arguments[0]` is how Selenium passes in the callback for `execute_async_script()`.
injected_javascript = (
	'const callback = arguments[0];'
	'const handleDocumentLoaded = () => {'
	'  Object.defineProperty(navigator, "webdriver", { get: () => false, });'
	'  Object.defineProperty(navigator, "languages", { get: () => ["en-US", "en", "es"], });'
	'  Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3, 4, 5], });'
	'  callback();'
	'};'
	'if (document.readyState === "loading") {'
	'  document.addEventListener("DOMContentLoaded", handleDocumentLoaded);'
	'} else {'
	'  handleDocumentLoaded();'
	'}'
)

def inject_js():
	options = webdriver.ChromeOptions()
	options.add_argument('--no-sandbox')
	options.add_argument('--window-size=1420,1080')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
	driver = webdriver.Chrome(chrome_options=options)

	inject_js_with_driver(driver)

	# Cleanup the driver before the next test.
	driver.quit()


def take_snapshot(driver):
	# Save the results as an image
	filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ".png"
	driver.get_screenshot_as_file(filename)


def inject_js_with_driver(driver):
	# Navigate to the test page and inject the JavaScript.
	driver.get(URL)
	# waiting for all of these resources to load before executing the JavaScript
	driver.execute_async_script(injected_javascript)

	html_source = driver.page_source
	logger.info('leboncoin: html_source + injected JS: %s', html_source)

	# take_snapshot(driver)
