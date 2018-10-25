from bs4 import BeautifulSoup
import requests
import time
import datetime

songlist = []

def songget():
	req = requests.get('https://www.bbc.co.uk/6music')
	soup = BeautifulSoup(req.text,'html.parser')

	songinfo = {'Song Name': soup.find('div', {'class':'on-air__track-now-playing__title'}).text, 'Artist': soup.find('div', {'class':'on-air__track-now-playing__artist'}).text}
	if songinfo not in songlist:
		with open('songlist.txt','a') as songtxt:
			songtxt.write('%s\n' % songinfo)
		songlist.append(songinfo)
		print(songinfo)
	
	time.sleep(60)
	songget()


songget()