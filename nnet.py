import keras as kr
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
import PIL
import numpy as np
import os
from keras.models import load_model


#trains a network on a selected set of data with a fixed neural network architecture
#takes in an array of paths to picture file folders
#inpath - images that are the object
#dpath - images that are not the object
#outpath - network output path
#netDim dimension of the training images
def trainNetwork(inPath,dpath,outPath,netDim,eph):
	net = Sequential()
	net.add(Conv2D(64,kernel_size=3,activation='relu',input_shape=(netDim,netDim,1)))
	net.add(MaxPooling2D(pool_size=(2,2)))
	net.add(Conv2D(64,kernel_size=3,activation='relu'))
	net.add(MaxPooling2D(pool_size=(2,2)))
	net.add(Conv2D(64,kernel_size=3,activation='relu'))
	net.add(MaxPooling2D(pool_size=(2,2)))
	net.add(Flatten())
	net.add(Dense(1,activation='sigmoid'))
	net.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

	xtrain = []
	ytrain = []

	tlist = []
	tflist = []
	
	for fp in inPath:
		for filename in os.listdir(fp):
			tlist.append(fp+filename)

	for fp in dpath:
		for filename in os.listdir(fp):
			tflist.append(fp+filename)

	for a in range(0,len(tlist)):
		wimg = PIL.Image.open(tlist[a]).convert("L")
		wimg = wimg.resize((netDim,netDim))
		wia = np.asarray(wimg)
		wia = wia.astype("float32")
		wia = wia / 255.0
		xtrain.append(wia)
		ytrain.append([1.0])

	for a in range(0,len(tflist)):
		wimg = PIL.Image.open(tflist[a]).convert("L")
		wimg = wimg.resize((netDim,netDim))
		wia = np.asarray(wimg)
		wia = wia.astype("float32")
		wia = wia / 255.0
		xtrain.append(wia)
		ytrain.append([0.0])

	xtrain = np.array(xtrain)
	ytrain = np.array(ytrain)
	xtrain = np.reshape(xtrain,((len(tlist)+len(tflist)),netDim,netDim,1))
	net.fit(xtrain,ytrain,epochs=eph)
	net.save(outPath)
	return 


#loads the network from the file and checks if the image contains the object the network was trained to detect
#outputs a value from 0 to 1.
#input nethwork path, image dimensions the network was trained on
class cnnNet:
	def __init__(self,netPath,netDim):
		self.net = load_model(netPath)
		self.netDim = netDim

	#check if the image contains an object the network was trained to detect
	def checkImage(self,img):
		wimg = img
		wimg = wimg.resize((self.netDim,self.netDim))
		wia = np.asarray(wimg)
		wia = wia.astype("float32")
		wia = wia / 255.0
		xdta = []
		xdta.append(wia)
		xdta = np.array(xdta)
		xdta = np.reshape(xdta,(1,self.netDim,self.netDim,1))
		rz = self.net.predict(xdta)
		return float(rz[0])

	#test network on images in a folder
	def testNet(self,testPath):
		tf = []
		for fp in testPath:
			for filename in os.listdir(fp):
				tf.append(fp+filename)
		for a in range(0,len(tf)):
			wimg = PIL.Image.open(tf[a]).convert("L")
			pb = self.checkImage(wimg)
			print(tf[a],"->",pb)
		return 

	#traverse the input image in strides and check if any contains any objects
	#otputs a buffers of detected images, their coordinates, and the network outputs
	#obBuf - PIL images croped from the main image
	#cordBuf - PIL image coordinates on the main image
	#pbBuf - Network output neuron value
	def findAllObjects(self,img,stride,rpb):
		obBuf = []
		cordBuf = []
		pbBuf = []
		x = 0
		y = 0
		aimg = img.convert("L")
		while( x < img.width):
			while(y < img.height):
				if(x+self.netDim < img.width and y+self.netDim < img.height):
					wimg = aimg.crop((x,y,x+self.netDim,y+self.netDim))
					pb = self.checkImage(wimg)
					if(pb >= rpb):
						print(x,y)
						cimg = img.crop((x,y,x+self.netDim,y+self.netDim))
						obBuf.append(cimg)
						cordBuf.append((x,y))
						pbBuf.append(pb)
				y += stride
			y = 0
			x += stride
		return (obBuf,cordBuf,pbBuf)
