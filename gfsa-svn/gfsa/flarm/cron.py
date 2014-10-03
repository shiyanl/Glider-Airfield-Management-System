import urllib2

def update_flarm():
	urllib2.urlopen('http://localhost:80/flarm_api')

def update_flarm_all():
	urllib2.urlopen('http://localhost:80/flarm_api_all')