# coding: utf-8

import csv
import os
import os.path
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client.house

@app.route('/')
def index():

	code = """ 
			function send(){
				$.ajax({
					type: "get",
					url: "http://localhost:8000/api",
					success:function(data)
					{
						//console.log the response
						//console.log(data);

						if (data) {
						    var i;
							for (i = 0; i < data.length; i++) {
							    window.open(data[i], '_blank');
							}
						}

						//Send another request in 60 seconds.
						setTimeout(function(){
							send();
						}, 60 * 1000);
					}
				});
			}
			send();
	"""

	return """<head>
				<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
			  </head>
				Polling...
				<script>{}</script>""".format(code)


@app.route('/api', methods = ['GET', 'POST'])
def api():
	# file_path = 'to_open_in_browser.csv'

	cursor = db.urls.find()
	urls = [c['url'] for c in cursor]

	if len(urls) == 0:
		return jsonify({})

	db.urls.remove({})

	return jsonify(urls)

	
	# if not os.path.exists(file_path):
	# 	return jsonify({})

	# with open(file_path, 'r') as f:
	# 	urls = csv.reader(f)
	# 	url = [item[0] for item in urls]

	# os.remove(file_path)

	# return jsonify(url)


if __name__ == '__main__':
	app.run(host='0.0.0.0', use_reloader=True)
