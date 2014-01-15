"""
Python file intended to scrape the Florida Governments page of inmates
and convert the data into a usable format

Written for Civis Analystics
By Andrew Gilchrist-Scott
"""
from bs4 import BeautifulSoup
import requests
import re
import glob

def main():

	url = raw_input("Enter the website to extract urls: ")
	reader = open('test.txt', 'a+')

	if "http://" not in url:
		url = "http://" + url

	req = requests.get(url)

	data = req.text

	soup = BeautifulSoup(data)

	links = []

	for link in soup.find_all(['a','b']):
		links.append(link.get('href'))
		reader.write(link.get('href') + '\n')

	for link in links:
		if link[1:3] != 'gal':
			continue
		full = url + link
		newreq = requests.get(full)
		fulldat = newreq.text
		newsoup = BeautifulSoup(fulldat)
		for sublink in newsoup.find_all('a'):
			reader.write(sublink.get('href') + '\n')

main()