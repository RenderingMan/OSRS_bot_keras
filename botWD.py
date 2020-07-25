import wc
import imf
import ca
import time
import random
import nnet
import inv
import PIL


#copper powerminer script
class PowerMineBotNN:

	#takes the main windowing class as input
	def __init__(self,rsWindow):
		self.rsw = rsWindow
		#load the ore detecting neural net
		self.nn = nnet.cnnNet("./networks/oreRocksNet42",42)

		#hardcoded pixel values
		self.copperColor = [(54,34,19),(88,57,31),
		(98,64,34),(75,48,26),(107,70,38),
		(142,102,66),(131,94,60),
		(106,76,48),(112,81,52),(102,73,46),
		(87,63,40),(80,57,36),(40,29,17),
		(102,73,46),(131,94,60)]

		#high intensity points on a laplace filtered ore image
		#used to detect ores in the inventory
		self.orePoints = ((10,8),(18,20),(24,14),(26,15),(10,28))
		self.iv = inv.Inventory(self.rsw)

		self.tts = 0
		self.netDim = 42

	def checkRange(self,a,b,rg):
		for d in range(0,3):
			e = a[d] - b[d]
			if(abs(e) > rg):
				return 0
		return 1

	#detect pixels in a picture
	#pixel values as a list of rgb tuples (R,G,B)
	def findPixels(self,img,colorList,rg):
		pixelList = []
		dta = img.load()
		for x in range(0,img.width):
			for y in range(0,img.height):
				p = dta[x,y]
				for a in colorList:
					if(self.checkRange(p,a,rg) == 1):
						pixelList.append((x,y))
		return pixelList

	def clickCopperOre(self):
		self.rsw.getFrame()
		gc = self.rsw.ga
		(ob,cb,pb) = self.nn.findAllObjects(gc,14,0.9)
		print("Found ores:"+str(len(ob)))

		copperList = []

		indx = 0
		for a in ob:
			pl = self.findPixels(a,self.copperColor,3)
			if(len(pl) > 0):
				copperList.append((a,cb[indx],pb[indx],pl))
			indx+=1

		indx = 0
		rindx = 0

		dist = 10000

		for a in copperList:
			cd = a[1]
			d = self.rsw.distCtrGac(cd)
			if(d < dist):
				dist = d
				indx = rindx
			rindx+=1

		#select a random pixel detected on the ore rock and click on it
		if(len(copperList) == 0):
			print("Did not find ores")
			return
		oc = copperList[indx]
		pixel = oc[3][random.randint(0,len(oc[3])-1)]
		rx = pixel[0]+oc[1][0]
		ry = pixel[1]+oc[1][1]
		self.rsw.clickGS((rx,ry),"left")

	#drops mined ore from the inventory
	def dropOre(self):
		items = self.iv.getItems()
		indx = 0;
		for a in items:
			itm = self.iv.findItemPoints(a,self.orePoints)
			if(itm == 1):
				(x,y) = self.iv.getItemCoord(indx)
				print("dropping:" + str(x) + "-" + str(y) +" "+ str(indx))
				x += random.randint(0,10)
				y += random.randint(0,12)
				time.sleep(random.randint(1,4))
				self.rsw.clickINV((x,y),"right")
				time.sleep(random.randint(1,3))
				x += random.randint(-2,2)
				y += 44
				self.rsw.clickINV((x,y),"left")
			indx+=1

	def updateState(self):
		self.rsw.getFrame()
		self.dropOre()
		self.clickCopperOre()

	def start(self):
		while(1):
			self.updateState()
			time.sleep(random.randint(2,3))