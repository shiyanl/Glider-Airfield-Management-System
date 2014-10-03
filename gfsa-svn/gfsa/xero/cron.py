import urllib2

def compare_memeber():
	urllib2.urlopen('http://localhost:80/compare_members')

def send_notification():
	urllib2.urlopen('http://localhost:80/send_notification')

def update_contacts():
	urllib2.urlopen('http://localhost:80/update_contacts')

def update_itemcodes():
	urllib2.urlopen('http://localhost:80/update_itemcode')