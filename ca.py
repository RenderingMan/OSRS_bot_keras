import PIL
from PIL import ImageFilter
import random

#misc functions for pixel manipulation


#Need to implement pixel skipping
def writeBorderBox(img,pos,bw,v):
	dta = img.load()
	for a in range(pos[0],pos[2]):
		for b in range(pos[1],pos[3]):
			sza = pos[2] - a
			szb = pos[3] - b
			szc = abs(pos[0] - a)
			szd = abs(pos[1] - b)
			if(sza < bw or szb < bw or szc < bw or szd < bw):
				dta[a,b] = v



