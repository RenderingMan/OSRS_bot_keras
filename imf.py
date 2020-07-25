#image filters

import PIL
from PIL import ImageFilter

def laplaceFilter(img):
	laplacian = (-1,-1,-1, -1,8,-1, -1,-1,-1)
	lf = img.filter(ImageFilter.Kernel((3,3), laplacian,1,0))
	return lf

def laplaceFilterX(img,x):
	v = img;
	for a in range(0,x):
		z = laplaceFilter(v);
		v = z		
	return v

def sobelX(img):
	sobel = (-1,-2,-1, 0,0,0, 1,2,1)
	lf = img.filter(ImageFilter.Kernel((3,3), sobel,1,0))
	return lf

