# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)

def elastic_insert(nome,sobrenome,ElkIP):

	es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	    'timestamp': datetime.now(),
	}

	res = es.index(index="usuario", body=doc)
	print(res['result'])

	#res = es.get(index="usuario", doc_type='tweet', id=1)
	#print(res['_source'])

	es.indices.refresh(index="usuario")

def elastic_search(nome,sobrenome,ElkIP):
	es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	}

	print "\n\n" + str(doc) + "\n\n" 
	#res = es.search(index="usuario", body={"query": {"query_string": { "query": "nome: \"%(nome)s\" OR sobrenome: \"%(sobrenome)s\""}}})
	res = es.search(index="usuario", body={"query": {"match_all": {}}})
	print "\n\n" + str(res) + "\n\n" 
	print("Got %d Hits:" % res['hits']['total']['value'])
	result_list = []
	for hit in res['hits']['hits']:
		print("%(timestamp)s Nome: %(nome)s e Sobrenome: %(sobrenome)s" % hit["_source"])
		result_list.append("%(timestamp)s Nome: %(nome)s e Sobrenome: %(sobrenome)s" % hit["_source"])
	return result_list

@app.route('/')
def home():
	# serve index template
	return render_template('index.html', name='It\'s Alive')

@app.route('/update',methods= ['POST'])
def update():
	ElkIP = request.form['ElkIP']
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	elastic_insert(firstName,lastName,ElkIP)
	output = firstName + " " + lastName
	print "O IP do servidor e " + ElkIP
	print "O nome do individuo e " + output
	if firstName and lastName:
		return jsonify({'output':'Full Name: ' + output})
	return jsonify({'error' : 'Missing data!'})

@app.route('/search',methods= ['POST'])
def search():
	print request.form
	ElkIP = request.form['ElkIP']
	firstName = request.form['searchfirstName']
	lastName = request.form['searchlastName']
	search_result = elastic_search(firstName,lastName,ElkIP)
	output = str(search_result)
	#output = firstName + " " + lastName
	#print "O IP do servidor e " + ElkIP
	#print "O nome do individuo e " + output
	if search_result:
	#if firstName and lastName:
		return jsonify({'output':'Search Result: ' + output})
	return jsonify({'error' : 'Missing data!'})

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)