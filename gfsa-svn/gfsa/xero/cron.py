import urllib2

def compare_memeber():
	urllib2.urlopen('http://127.0.0.1:80/compare_members')

def send_notification():
	urllib2.urlopen('http://127.0.0.1:80/send_notification')

def update_contacts():
	urllib2.urlopen('http://127.0.0.1:80/update_contacts')

def update_itemcodes():
	urllib2.urlopen('http://127.0.0.1:80/update_itemcode')