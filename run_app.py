# coding: utf-8

import csv
import yaml
import os
import os.path
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client.house

with open("config.yml", 'r') as f:
	config = yaml.load(f)
searches = config['data']


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
				<script>{1}</script>
		   """.format(str(search_city), code_check_api + code_check_last)


@app.route('/api/<city>')
def api(city):
	cursor = db.urls.find({'city': city})
	urls = [c['url'] for c in cursor]

	if len(urls) == 0:
		return jsonify({})

	db.urls.remove({'city': city})

	return jsonify(urls)


@app.route('/clean/<city>')
def clean(city):
	db.urls.remove({'city': city})

	return jsonify({'status': 'ok', 'removed_city': city})


@app.route('/last/<city>')
def last(city):
	cursor = db.last_check.find({'city': city})
	items = [c['city'] + ' - ' + c['site'] + ' - ' + c['date'] for c in cursor]

	return jsonify(items)


if __name__ == '__main__':
	app.run(host='0.0.0.0', use_reloader=True)
