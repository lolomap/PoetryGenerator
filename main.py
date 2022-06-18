# -*- coding: utf-8 -*-

import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from pyswip import Prolog

hostName = 'localhost'
serverPort = 8080

prologobj = Prolog()
# prologobj.consult('util.pl', 'words.pl')


def PrologInit(prolog):
	for _ in prolog.query('use_module(library(clpfd)).'):
		pass
	for _ in prolog.query('[util].'):
		pass
	for _ in prolog.query('[words].'):
		pass


def GenText(prolog, word, pos, speech_part):
	for item in prolog.query('call_nth(рифма(Стих, ' + word + ', ' + str(speech_part) + '), ' + str(pos) + ').'):
		res = ''
		for line in item['Стих']:
			for word in line:
				res += word + ' '
			res = res[:-1]
			res += '\n'
		res = res[:-1]
		return res
	return ''


def GenSimple(prolog, pos):
	for item in prolog.query('call_nth(одно(Стих, ' + str(random.randint(0, 3)) + '), ' + str(pos) + ').'):
		res = ''
		for line in item['Стих']:
			for word in line:
				res += str(word) + ' '
			res = res[:-1]
			res += '\n'
		res = res[:-1]
		# print(item)
		return res
	return ''


class WebServer(BaseHTTPRequestHandler):

	def do_GET(self):
		# ShuffleDict()
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(bytes('{"text": "'+GenSimple(prologobj, 1)+'"}', 'utf-8'))

	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
		raw = self.rfile.read(content_length).decode('utf-8')
		# print(raw)
		post_data = json.loads(raw)
		n = random.randint(0, 1000000)
		if post_data['pos'] != -1:
			n = post_data['pos']

		resText = GenText(prologobj, post_data['data'], n, post_data['speech_part'])

		self.wfile.write(bytes(
			'{"text": "' + resText +
			'", "max_count": ' + str(n) + '}', 'utf-8')
		)


if __name__ == '__main__':
	PrologInit(prologobj)
	print('Prolog initialized')

	webServer = HTTPServer((hostName, serverPort), WebServer)
	print('Server running')

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print('Server stopped')
