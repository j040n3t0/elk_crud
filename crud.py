# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)

######### Funções

def elastic_insert(nome,sobrenome,ElkIP):

	es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	    'timestamp': datetime.now(),
	}

	res = es.index(index="usuarios", body=doc)
	print(res['result'])

	#res = es.get(index="usuarios", doc_type='tweet', id=1)
	#print(res['_source'])

	es.indices.refresh(index="usuarios")

def elastic_search(nome,sobrenome,ElkIP):
	es = Elasticsearch([ElkIP])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	}

	print "\n\n" + str(doc) + "\n\n"
	sobrenome = str(doc['sobrenome'])
	nome = str(doc['nome'])
	print sobrenome
	print nome
	if nome == "all" or sobrenome == "all":
		res = es.search(index="usuarios", body={"query": {"match_all": {}}})
		#res = es.search(index="usuarios", body={"query": {"query_string": { "query": "nome: %s AND sobrenome: %s" % (nome,sobrenome)}}})
	else:
		res = es.search(index="usuarios", body={"query": {"query_string": { "query": "nome: %s AND sobrenome: %s" % (nome,sobrenome)}}})
	#	res = es.search(index="usuarios", body={"query": {"match_all": {}}})
	#print "\n\n" + str(res) + "\n\n" 
	print("Got %d Hits:" % res['hits']['total']['value'])
	result_list = []
	for hit in res['hits']['hits']:
		print hit
		#print "ID: %s " % hit["_id"]
		print("ID: %s | Nome: %s e Sobrenome: %s" % (hit["_id"], hit["_source"]["nome"],hit["_source"]["sobrenome"]))
		result_list.append("ID: %s | Nome: %s e Sobrenome: %s" % (hit["_id"], hit["_source"]["nome"],hit["_source"]["sobrenome"]))
	return result_list

def elastic_update(id,nome,sobrenome,ElkIP):
	es = Elasticsearch([ElkIP])
	#es = Elasticsearch(['10.0.1.69'])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	}

	res = es.index(index="usuarios", id=id, body=doc)
	print(res['result'])

def elastic_delete(id,nome,sobrenome,ElkIP):
	es = Elasticsearch([ElkIP])
	#es = Elasticsearch(['10.0.1.69'])

	doc = {
	    'nome': nome ,
	    'sobrenome': sobrenome,
	}

	res = es.delete(index="usuarios", id=id)
	print(res['result'])

#####################################

@app.route('/')
def home():
	# serve index template
	return render_template('index.html', name='It\'s Alive')

@app.route('/insert',methods= ['POST'])
def insert():
	ElkIP = request.form['ElkIP']
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	elastic_insert(firstName,lastName,ElkIP)
	output = firstName + " " + lastName
	#print "O IP do servidor e " + ElkIP
	#print "O nome do individuo e " + output
	if firstName and lastName:
		return jsonify({'output':'Dado inserido: ' + output})
	return jsonify({'output' : 'Nenhum dado encontrado!'})

@app.route('/search',methods= ['POST'])
def search():
	#print request.form
	ElkIP = request.form['ElkIP']
	firstName = request.form['searchfirstName']
	lastName = request.form['searchlastName']
	search_result = elastic_search(firstName,lastName,ElkIP)
	#output = str(search_result)
	#print search_result
	output = search_result

	try:
		return jsonify({'output': output[0]
		})
	except:
		return jsonify({'output' : 'Nenhum dado encontrado!'})

@app.route('/update',methods= ['POST'])
def update():
	#print request.form
	ElkIP = request.form['ElkIP']
	id_user = request.form['id_user']
	nome_user = request.form['nome_user']
	sobrenome_user = request.form['sobrenome_user']
	elastic_update(id_user,nome_user,sobrenome_user,ElkIP)
	return jsonify({'output' : 'Valor atualizado!'})

@app.route('/delete',methods= ['POST'])
def delete():
	#print "\n\nChamou o DELETE\n\n"
	#print request.form
	ElkIP = request.form['ElkIP']
	id_user = request.form['id_user']
	nome_user = request.form['nome_user']
	sobrenome_user = request.form['sobrenome_user']
	elastic_delete(id_user,nome_user,sobrenome_user,ElkIP)
	return jsonify({'output' : 'Valor removido!'})

if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)