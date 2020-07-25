from Xlib.display import Display
from PIL import Image
import Xlib
import PIL
from Xlib.ext.xtest import fake_input
import pyautogui
import math
import time
import sys

def traverseWindows(window,wmName,obRt):
	children = window.query_tree().children
	for w in children:
		if(w.get_wm_name() == wmName):
			obRt[0] = w
		traverseWindows(w,wmName,obRt)

def findWindowByName(window,wmName):
	rtl = [0]
	traverseWindows(window,wmName,rtl)
	return rtl[0]

def copyScreenImageFile(window,name):
	wSz = window.get_geometry()
	x = wSz.width
	y = wSz.height

	raw = window.get_image(0, 0, x,y, Xlib.X.ZPixmap, 0xffffffff)	
	pc = PIL.Image.frombytes("RGB", (x, y), raw.data, "raw", "BGRX")
	pc.save("./"+name+".png")


#scrape window
#takes its xlib window handle
def copyScreenImage(window):
	wSz = window.get_geometry()
	x = wSz.width
	y = wSz.height
	raw = window.get_image(0, 0, x,y, Xlib.X.ZPixmap, 0xffffffff)	
	pc = PIL.Image.frombytes("RGB", (x, y), raw.data, "raw", "BGRX")
	return pc


class RsWindow:
#800x600 is the default size the bot uses, when it gets the window handle it resizes the window to that size
#This class takes care of getting the runescape window handle and window pixel buffer scraping/manipulating/window input
#it also has hardcoded coordinates on the window that splits the game UI in to elements that get scrapped.	
	def __init__(self):
		display = Display()
		#get base window handle
		root = display.screen().root
		self.dsp = display
		self.rt = root

		#traverse windows and find the runescape window by name
		self.window = findWindowByName(root,"Old School RuneScape")
		if(self.window == 0):
			print("Cant find Oldschool Runescape window")
			sys.exit(0)
		#resize the window to set dimensions, all of the in game GUI offsets are hardcoded
		self.window.configure(width=800,height=600)
		#wait till the window is resized (I know)		
		time.sleep(5)
		self.frame = 0
		self.inv = 0
		self.map = 0
		self.ga = 0;
		self.txt = 0;

		self.ctrGac = (246,165)

		#ingame GUI offsets
		
		#game area (game world window)
		self.gac = (20,4, 511,333)
		#inventory
		self.invc = (567,208, 746,463)
		#map
		self.mapc = (582,3, 727,157)
		#text/chat area
		self.txtc = (21,341, 507,452)

	#distance from game area center
	def distCtrGac(self,cordTuple):
		dx = self.ctrGac[0] - cordTuple[0]
		dy = self.ctrGac[1] - cordTuple[1]
		dist = math.sqrt(dx*dx + dy*dy)
		return dist

	#scrape the current window frame and save it in the frame variable
	#other modules/scripts will use this frame for image processing
	def getFrame(self):
		self.frame = copyScreenImage(self.window)
		self.ga = self.frame.crop(self.gac)
		self.inv = self.frame.crop(self.invc)
		self.map = self.frame.crop(self.mapc)
		self.txt = self.frame.crop(self.txtc)
		return self.frame

	#click on game world area
	#gets global window coordinates and calculates the global screen position needed for pyautogui
	#takes in local game world area coordinates
	def clickGS(self,cord,btn):
		parent = self.window.query_tree().parent
		pg = parent.get_geometry()

		rx = cord[0]+pg.x+18
		ry = cord[1]+pg.y+24

		#dont need to move the pointer
		pyautogui.moveTo(rx, ry)
		pyautogui.click(button=btn,x=rx,y=ry)


	#mouse click in the inventory
	def clickINV(self,cord,btn):
		parent = self.window.query_tree().parent
		pg = parent.get_geometry()

		rx = cord[0]+pg.x+18+self.invc[0]
		ry = cord[1]+pg.y+24+self.invc[1]

		#dont need to move the pointer
		pyautogui.moveTo(rx, ry)
		pyautogui.click(button=btn,x=rx,y=ry)
			
	#save entire window frame to disk
	def saveFrame(self,name):
		copyScreenImageFile(self.window,name)