import six.moves.urllib.parse as urlparse
import requests

class spotapi(object):

	def authenticate(client_id, client_sec, redirect_uri, scope):
		params = {
			'client_id': client_id,
			'client_sec': client_sec,
			'response_type': 'code',
			'redirect_uri': redirect_uri,
			'scope': scope
			}

		urlparams = urlparse.urlencode(params)
		import webbrowser
		webbrowser.open('https://accounts.spotify.com/authorize/?' + urlparams)
		code = input('Enter URL: ').split('?code=')[1]
		import base64
		baseclient = base64.b64encode((params['client_id'] + ':' + params['client_sec']).encode())
		headers = {
			'Authorization': 'Basic ' + baseclient.decode('ascii')
		}

		params = {
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': redirect_uri
		}

		urlparams = urlparse.urlencode(params)
		tokenreq = requests.post('https://accounts.spotify.com/api/token/', data=params, headers=headers).json()
		return tokenreq['access_token']

	def search(token, **kwargs):

		args = locals()

		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + token
		}

		query = {
		'q': None,
		'type': None, 
		'limit': '5',
		'market': 'GB'
		}

		try:
			if kwargs.get('track') and kwargs.get('artist'):
				query['q'] = 'track: %s artist: %s' % (kwargs.get('track'), kwargs.get('artist'))
				query['type'] = 'track,artist'
			elif kwargs.get('track'):
				query['q'] = '%s' % kwargs.get('track')
				query['type'] = 'track'
			elif kwargs.get('artist') and kwargs.get('album'):
				query['q'] = 'album: %s artist: %s' % (kwargs.get('album'), kwargs.get('artist'))
				query['type'] = 'album,artist'
			elif kwargs.get('artist'):
				query['q'] = '%s' % kwargs.get('artist')
				query['type'] = 'artist' 
			elif kwargs.get('album'):
				query['q'] = '%s' % kwargs.get('album')
				query['type'] = 'album' 
		except Exception as e:
			raise('Error', e)  # This part needs some work done to it

		if kwargs.get('limit'):
			query['limit'] = kwargs.get('limit')
		
		urlparams = urlparse.urlencode(query)

		songjson = requests.get('https://api.spotify.com/v1/search?%s' % urlparams, headers=headers).json()
		
		return songjson

	def addplaylist(token, json, playlist_id):

		urilist = []

		for x in str(json).split("'uri': '"):
			uri = x.split("'}")[0]
			if ':track' in uri:
				urilist.append(uri)

		headers = {
			'Authorization': 'Bearer ' + token,
		}

		uriadd = ','.join(urilist).replace(':','%3A')
		addpost = print(requests.post('https://api.spotify.com/v1/playlists/%s/tracks?uris=%s' % (playlist_id, uriadd), headers=headers))
