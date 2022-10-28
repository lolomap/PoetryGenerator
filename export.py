# -*- coding: utf-8 -*-

import pymysql

vowels = 'ёуеыаоэяию'

text = ''

connection = pymysql.connect(user='poetry', password='3WskCJ_0789', database='poetrydb', unix_socket="/var/run/mysqld/mysqld.sock")
try:
	with connection.cursor(pymysql.cursors.DictCursor) as cursor:
		sql = "SELECT * FROM WordsDictionary LIMIT 150000;"
		cursor.execute(sql)
		data = cursor.fetchall()
		# print(data)

		for item in data:
			if (item['SpeechPart'] == 1):
				text += 'прилагательное('
			elif (item['SpeechPart'] == 2):
				text += 'глагол('
			elif (item['SpeechPart'] == 3):
				text += 'существительное('
			elif (item['SpeechPart'] == 6):
				text += 'наречие('
			else:
				continue

			stress = 0
			i = 0
			for s in item['Text']:
				if s in vowels:
					stress += 1
					if item['StressPosition'] == i:
						break
				i += 1

			text += item['Text'] + ', ' + str(stress) + ').\n'
		with open('out.txt', 'w', encoding='utf8') as f:
			f.write(text)
finally:
	connection.close()
