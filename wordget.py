from bs4 import BeautifulSoup
import requests


req = requests.get('https://en.wikipedia.org/wiki/Special:Random')
soup = str(list(BeautifulSoup(req.text,'html.parser'))).lower().split() #Not pythonic?

exists = []
wordlist = []

try:
	with open('wordbank.txt','r') as bank:
		exists.extend(bank.read().splitlines())
except:
	pass

for char in soup:
	try:
		char.encode('ascii')
		if char.isalpha():
			wordlist.append(char)
		else:
			del char
	except:
		del char

combi = set(exists + wordlist)

try:
	with open('wordbank.txt','w') as bank:
		for word in combi:
			bank.write('%s\n' % word)
except:
	pass

"""Really inefficient. Makes a set from current word list and existing words list, then writes them all to the file instead of appending. This is the only way I can find at the moment which stops duplicate words being written. """










	














