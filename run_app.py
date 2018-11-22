# coding: utf-8
import csv
import datetime
import yaml
import os
import os.path
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

from utils import get_db, get_config, load_config_to_mongo, configure_logger

logger = configure_logger('housing_bot')

app = Flask(__name__)

load_config_to_mongo()
db = get_db()
searches =list(db.config.find({}, {'_id': 0}))


@app.route('/')
def index_0():
	search_cities = ["<a href='/{city}'>{city}</a>".format(city=s['city']) for s in searches]
	
	return '<h1>Please choose a search</h1>' + str(search_cities)


@app.route('/<city>')
def index(city):

	code_check_api = """ 
			function check_api(){{
				$.ajax({{
					type: "get",
					url: "/api/{city}",
					success:function(data)
					{{
						if (data) {{
							var i;
							for (i = 0; i < data.length; i++) {{
								window.open(data[i], '_blank');
							}}
						}}

						//Send another request in 60 seconds.
						setTimeout(function(){{
							check_api();
						}}, 60 * 1000);
					}}
				}});
			}}
			check_api();
	""".format(city=city)

	code_check_last = """ 
			function check_last(){{
				$.ajax({{
					type: "get",
					url: "/last/{city}",
					success:function(data)
					{{
						if (data) {{
							var i;
							for (i = 0; i < data.length; i++) {{
								console.log(data[i]);
							}}
						}}

						$('#p_last_check').html('<p style="background-color:red;">Error</p>')
						if (data.length > 0) {{		
							$('#p_last_check').html('<p style="background-color:green;">Running...</p>')
						}}

						//Send another request in 60 seconds.
						setTimeout(function(){{
							check_last();
						}}, 60 * 1000);
					}}
				}});
			}}
			check_last();
	""".format(city=city)

	search_city = [s for s in searches if s['city'] == city]

	return """<head>
				<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
			  </head>
				{0}
				<br><p id="p_last_check"></p>
				<script>{1}</script>
		   """.format(str(search_city), code_check_api + code_check_last)


@app.route('/api/<city>')
def api(city):
	db = get_db()
	cursor = db.urls.find({'city': city})
	urls = [c['url'] for c in cursor]

	if len(urls) == 0:
		return jsonify({})

	db.urls.remove({'city': city})

	logger.info('Removed urls for: %s', city)

	return jsonify(urls)


@app.route('/clean/<city>')
def clean(city):
	db = get_db()
	db.urls.remove({'city': city})

	logger.info('Removed urls for: %s', city)

	return jsonify({'status': 'ok', 'removed_city': city})


@app.route('/last/<city>')
def last(city):
	db = get_db()
	d = datetime.datetime.now() - datetime.timedelta(minutes=10)
	# retourne les 10 dernieres min
	cursor = db.last_check.find({'city': city, "date": {"$gt": d}}).sort("date")
	items = [c['city'] + ' - ' + c['site'] + ' - ' + c['date'].strftime("%Y-%m-%d %H:%M") for c in cursor]

	return jsonify(items)


if __name__ == '__main__':
	app.run(host='0.0.0.0', use_reloader=True)
