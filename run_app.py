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

@app.route('/')
def index():

	code_check_api = """ 
			function check_api(){
				$.ajax({
					type: "get",
					url: "/api",
					success:function(data)
					{
						if (data) {
						    var i;
							for (i = 0; i < data.length; i++) {
							    window.open(data[i], '_blank');
							}
						}

						//Send another request in 60 seconds.
						setTimeout(function(){
							check_api();
						}, 60 * 1000);
					}
				});
			}
			check_api();
	"""

	code_check_last = """ 
			function check_last(){
				$.ajax({
					type: "get",
					url: "/last",
					success:function(data)
					{
						if (data) {
						    var i;
							for (i = 0; i < data.length; i++) {
							    console.log(data[i]);
							}
						}

						//Send another request in 60 seconds.
						setTimeout(function(){
							check_last();
						}, 60 * 1000);
					}
				});
			}
			check_last();
	"""

	return """<head>
				<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
			  </head>
			    {0}
				<script>{1}</script>
		   """.format(str(config['data']), code_check_api + code_check_last)


@app.route('/api')
def api():
	cursor = db.urls.find()
	urls = [c['url'] for c in cursor]

	if len(urls) == 0:
		return jsonify({})

	db.urls.remove({})

	return jsonify(urls)


@app.route('/clean')
def clean():
	db.urls.remove({})

	return jsonify({'status': 'ok'})


@app.route('/last')
def last():
	cursor = db.last_check.find()
	items = [c['city'] + ' - ' + c['site'] + ' - ' + c['date'] for c in cursor]

	# if len(items) == 0:
	# 	return jsonify({})

	return jsonify(items)


if __name__ == '__main__':
	app.run(host='0.0.0.0', use_reloader=True)
