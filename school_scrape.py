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
#import re
#import glob
#import time
#import os
from subprocess import call
from math import *
from decimal import *

def main():

	fromfilename = r"HSReportCard.csv"
	filename = r'Chischools.txt'
	writer = open(filename, 'w+')
	writer.close()

	#inp = ["csvcut", "-c", "2,57,58,26", fromfilename]
	#inp2 = ["|", "sed", ">", filename]

	#call(inp, inp2)

	reader = open(fromfilename, 'r')

	rawschools = []
	schools = []
	ind = 0
	for line in reader:
		line.strip()
		''' School specific " deletion
		if not line[7].isalpha():
			ind3 = 8
			while line[ind3] != line[7]:
				ind3 += 1
			rawschools.append([line[0:5]])
			rawschools[ind].append(line[7:ind3+1])
			newline = line[ind3+2:].split(',')
			for item in newline:
				rawschools[ind].append(item)
		else:
			rawschools.append(line.split(','))
		'''
		rawschools.append(line.split('.'))
		'''
		schools.append([rawschools[ind][1],rawschools[ind][58], \
			rawschools[ind][59], rawschools[ind][25]])
		'''
		ind += 1

	reader.close()

	'''
	schools[0].append("Min distance to other school")

	for x in range(1,len(schools)):
		minval = 100000000000000000000000000000000000;
		for y in range(1,len(schools)):
			if y == x:
				continue
			dist = distance(Decimal(schools[x][1]), Decimal(schools[x][2]), \
				Decimal(schools[y][1]), Decimal(schools[y][2]))
			if dist < minval:
				minval = dist
		schools[x].append(minval)
		
	
	for x in schools:
		print x[0], ",", x[4], ",", x[3]

	schools = removeBlanks(schools)

	distances = []
	ACT = []
	for school in schools:
		distances.append(school[4])
		ACT.append(school[3])
	'''

	sig = []
	twoVarStats(distances,ACT,sig)

	for x in range(len(rawschools[0])):
		for y in range(x+1, len(rawschools[0])):
			xls = []
			yls = []
			for school in rawschools:
				xls.append(school[x])
				yls.append(school[y])
			fail = removeIndividualBlanks(xls,yls)
			if fail:
				continue
			twoVarStats(xls,yls,sig)

	for item in sig:
		print "Significant relationship between", item[0], "and", item[1]
		print "\tr =", item[2]
		print "\tr^2 =", item[2]**2
	




def distance(x1,y1,x2,y2):
	dist = sqrt((x1-x2)**2 + (y1-y2)**2)
	return dist

def removeBlanks(lst):
	newlst = []
	for item in lst:
		blank = False
		for it in item:
			if it == None:
				blank = True
				break
			elif (it == '') or (it == ' '):
				blank = True
				break

		if not blank:
			newlst.append(item)

	return newlst

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

	print "Between", titlex, "and", titley, ":"
	print "\tr =", r
	print "\tr^2 =", r**2

	if r > .8 or r < -.8:
		#print "Significant relationship between", titlex, "and", titley
		#print
		sig.append((titlex, titley, r))

	return

main()