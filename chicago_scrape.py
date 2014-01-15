"""
Python file intended to scrape the Chicago city data page of school data
and put it into a usable format

Written for Civis Analystics
By Andrew Gilchrist-Scott
On the week of January 13-17, 2014

Assumes user has csvkit and 
"""
#from bs4 import BeautifulSoup
#import requests
import re
import glob
import time
import os
from subprocess import call

def main():

	fromfilename = r"HSReportCard.csv"
	reader = open(fromfilename, 'r')
	filename = r'Chischools.txt'
	writer = open(filename, 'w+')

	inp = ["csvcut", "-c", "2,59,60", fromfilename]

	writer.write(call(inp))



	reader.close()
	writer.close()

main()