from PIL import Image
import wc
import PIL
import imf
import math
import random

#item slot size in pixels at 800X600 
#x- 42 y - 36 

#used for inventory handling
#takes in RsWindow class as an argument
class Inventory:
	def __init__(self,rsw):
		self.rsw = rsw

	#traverses inventory and gets every item slot picture
	#returns PIL image objects in an array
	#total object number - 28
	def getItems(self):
		xc = 13
		yc = 5

		xcc = 44
		ycc = 36

		ia = []

		for y in range(0,7):
			for x in range(0,4):
				nx = xc+(x*42)
				ny = yc+(y*36)
				
				nxx = xcc+(x*42)
				nyy = ycc+(y*36)
				iimg = self.rsw.inv.crop((nx,ny,nxx,nyy))
				ia.append(iimg)
		return ia

	#checks edge detected picture and looks for points with > 50% intensity
	#used to find items with hardcoded coordinates
	#most items have high intensity points in specific coordinates
	def findItemPoints(self,img,pa):
		ga = img.convert("L")
		lp = imf.laplaceFilter(ga)
		lpd = lp.load()

		fp = 0

		for a in range(0,len(pa)):
			pv = lpd[pa[a][0],pa[a][1]]
			npv = pv/256
			if(npv > 0.5):
				fp+=1
		if(fp == len(pa)):
			return 1
		return 0

	#given the item number find the coordinates on the screen of the item in the inventory
	def getItemCoord(self,itemIndx):
		xc = 13
		yc = 5

		xcc = 44
		ycc = 36

		for y in range(0,7):
			for x in range(0,4):
				nx = xc+(x*42)
				ny = yc+(y*36)
				itm = (y*4)+x
				if(itm == itemIndx):
					return(nx,ny)

	#UNUSED:Tried to come up with some sort of an error tolerated unique item hash from the edge detected picture
	def findItemAvgVal(self,img,th):
		ga = img.convert("L")
		lp = imf.laplaceFilter(ga)
		lpd = lp.load()

		fp = 0

		for y in range(0,lp.height):
			for x in range(0,lp.width):
				pv = lpd[x,y]
				dist = x**2 + y**2
				vl = pv/256
				if(vl > th):
					fp += 1/dist
		return fp
