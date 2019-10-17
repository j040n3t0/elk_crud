# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys

app = Flask(__name__)


@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='It\'s Alive')

"""
@app.route('/receiver', methods = ['POST'])
def worker():
	#print request.form.to_dict()
	data = request.form.to_dict()
	#jsonData = jsonData.get_json()

	print data
	return jsonify({
		'data': render_template('response.html', data=data),
	})
	#return jsonify(success=True, data=jsonData)

	#print request.get_json()
	#data = request.get_json()
	#print "\n"
	#print data
	#print "IP ELASTICSEARCH.: " + data["IP"]
	#ip_elasticsearch = data["IP"]
"""
@app.route('/process',methods= ['POST'])
def process():
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	output = firstName + " " + lastName
	print "O nome do individuo e " + output
	if firstName and lastName:
		return jsonify({'output':'Full Name: ' + output})
	return jsonify({'error' : 'Missing data!'})


if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)