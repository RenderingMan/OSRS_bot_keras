import wc
import imf
from PIL import ImageFilter
import inv
import ca
import botWD
import nnet
import PIL
import sys

#train copper powerminer script neural network
def trainNetworks():
	trainImg = ["./images/oreRocks42/"]
	fi = ["./images/ground42/","./images/treeBase42/","./images/treeTop42/","./images/junk42/","./images/npc42/","./images/oreJunk42/"]
	nnet.trainNetwork(trainImg,fi,"./networks/oreRocksNet42",42,45)

for a in sys.argv:
	if(a == "-train"):
		trainNetworks()
		sys.exit(1)

#find osrs window handle
rsw = wc.RsWindow()

#create powerminer script instance
n = botWD.PowerMineBotNN(rsw)
#run indefinetly
n.start()
