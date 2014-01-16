"""
Python file intended to gather the data from a csv file from the Chicago
data portal and analyze it to find any interesting correlations

Written for Civis Analystics
By Andrew Gilchrist-Scott
On the week of January 13-17, 2014
"""
#from bs4 import BeautifulSoup
#import requests
#import re
#import glob
#import time
#import os
#from subprocess import call
from math import *
from decimal import *
import sys


def main():

	write = False
	if len(sys.argv) == 1:
		fromfilename = raw_input("Input the name of the csv file: ")
	elif len(sys.argv) == 2:
		if sys.argv[1][0] == '-':
			if sys.argv[1] == '-w':
				write = True
			else:
				print "Usage: chicago_scrape.py [-w] [filename.csv]"
				sys.exit(1)
		else:
			fromfilename = sys.argv[1]
	elif len(sys.argv) == 3:
		if sys.argv[1] == '-w':
			write = True
		else:
			print "Usage: chicago_scrape.py [-w] [filename.csv]"
			sys.exit(1)
		fromfilename = sys.argv[2]
	else:
		print "Usage: chicago_scrape.py [-w] [filename.csv]"
		sys.exit(1)

	try:
		reader = open(fromfilename, 'r')
	except:
		print "\nInvalid file name.\n"
		sys.exit(1)

	raw = []
	for line in reader:
		raw.append(line.strip().split(','))

	reader.close()

	ammendQuotes(raw)

	#Debugging tool
	'''
	for i in range(len(raw[0])):
		print i, raw[0][i]
		print "\t", raw[1][i] 
	n = len(raw[0])
	for row in raw:
		if len(row) != n:
			print "Length", len(row), "versus", n
			print row
	'''
	if write:
		writer = open(fromfilename[:-4] + 'Relationships.txt','w')

	for i in range(5):
		sig = []
		runStats(raw,sig)
		print
		print "Significant with", len(raw), "items:"
		for item in sig:
			print "Significant relationship between", item[0], "and", item[1]
			print "\tr =", item[2]
			print "\tr^2 =", item[2]**2
			if write: pen(writer,sig, len(raw))
		if (i < 4):
			raw = dropTen(raw)
	print
	if write:
		writer.close()
	return

def runStats(raw,sig):
	for x in range(len(raw[0])):
		for y in range(x+1, len(raw[0])):
			xls = []
			yls = []
			for item in raw:
				xls.append(item[x])
				yls.append(item[y])
			fail = removeIndividualBlanks(xls,yls)
			if fail:
				continue
			twoVarStats(xls,yls,sig)
	
def ammendQuotes(raw):
	for i in range(len(raw)):
		newrow = []
		ignore_ind = -1
		for j in range(len(raw[i])):
			if j <= ignore_ind:
				continue
			if "\"" not in raw[i][j]:
				newrow.append(raw[i][j])
			else:
				ignore_ind = j + 1
				newans = raw[i][j] + ','
				while "\"" not in raw[i][ignore_ind]:
					newans += raw[i][ignore_ind] + ','
					ignore_ind += 1
				newans += raw[i][ignore_ind]
				newrow.append(newans)
		raw[i] = newrow

def removeIndividualBlanks(x, y):
	newx = newy = []
	for i in range(len(x)):
		blank = False
		if (x[i] == None):
			if (y[i] == None):
				continue
			elif (y[i] == '') or (y[i] == ' '):
				continue
			else:
				return True
		elif (x[i] == '') or (x[i] == ' '):
			if (y[i] == None):
				continue
			elif (y[i] == '') or (y[i] == ' '):
				continue
			else:
				return True
		else:
			newx.append(x[i])
			newy.append(y[i])
	x = newx
	y = newy
	return False

def twoVarStats(x,y,sig):

	titlex = x[0]
	x = x[1:]
	titley = y[0]
	y = y[1:]

	if len(x) != len(y):
		print titlex, "and", titley, "not paired; cannot compute stats."
		return

	N = len(x)

	for i in range(N):
		xgood = False
		try:
			#print "tryx1", x[i]
			x[i] = Decimal(x[i])
			xgood = True
		except:
			#print "exceptx1", x[i]
			x[i] = x[i].strip(' %')
			if x[i][0:5] == 'Level':
				x[i] = x[i].strip('Level ')
		if not xgood:
			try:
				#print "tryx2", x[i]
				x[i] = Decimal(x[i])
			except:
				#print "exceptx2", x[i]
				#print titlex, "not of analyzable type"
				#print "Example:", x[i], type(x[i])
				return
		try:
			#print "tryy1", y[i]
			y[i] = Decimal(y[i])
			continue
		except:
			#print "except y1", y[i]
			y[i] = y[i].strip(' %')
			if y[i][0:5] == 'Level':
				y[i] = y[i].strip('Level ')
		try:
			#print "tryy2", y[i]
			y[i] = Decimal(y[i])
			continue
		except:
			#print "excepty2", y[i]
			#print titley, "not of analyzable type"
			#print "Example:", y[i], type(y[i])
			return

	sumx = Decimal(fsum(x))
	sumy = Decimal(fsum(y))
	xsq = []
	for item in x:
		xsq.append(item**2)
	"""
	#Linear Regression Section
	ysq = []
	for item in y:
		ysq.append(item**2)

	xy = []
	for i in range(N):
		xy.append(x[i]*y[i])

	sumxy = Decimal(fsum(xy))
	sumxsq = Decimal(fsum(xsq))
	sumysq = Decimal(fsum(ysq))

	b = (N*sumxy - sumx*sumy)/(N*sumxsq - sumx**2)
	a = (sumy - b*sumx)/N

	predy = []
	for i in range(N):
		predy.append(a + b*x[i])

	print "Linear regression: y =", a, "+", b, "* x"
	"""

	xbar = sumx/N
	ybar = sumy/N

	xydev = []
	xsqdev = []
	ysqdev = []
	for i in range(N):
		xydev.append((x[i] - xbar)*(y[i] - ybar))
		xsqdev.append((x[i] - xbar)**2)
		ysqdev.append((y[i] - ybar)**2)

	r = (fsum(xydev))/(sqrt(fsum(xsqdev))*(sqrt(fsum(ysqdev))))

	#print "Between", titlex, "and", titley, ":"
	#print "\tr =", r
	#print "\tr^2 =", r**2

	if r > .8 or r < -.8:
		#print "Significant relationship between", titlex, "and", titley
		#print
		sig.append((titlex, titley, r))

	return

def dropTen(lol):
	N = len(lol)
	ten = int(.1*N)
	tallyls = []
	for ls in lol:
		tally = 0
		for item in ls:
			if item == None:
				continue
			elif type(item) == type(''):
				if item.strip() == '':
					continue
			tally += 1
		tallyls.append(tally)
	old = list(tallyls)
	tallyls.sort()
	minval = tallyls[ten]
	newlol = []
	for i in range(len(lol)):
		if old[i] >= minval:
			newlol.append(lol[i])
	dropped = len(lol) - len(newlol)
	print "\n**Dropping the %d least responsive members" % dropped
	return newlol

def pen(writer, sig, n):
	writer.write("\nSignificant Relationships with %d items:" % n)
	for item in sig:
		writer.write("Significant relationship between %s and %s" 
			% (sig[0],sig[1]))
		writer.write("\tr = %d" % sig[2])
		writer.write("\tr^2 = %d" % sig[2]**2)
main()