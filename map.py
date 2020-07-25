import PIL


#was supposed to be map navigation mechanisim
#didint get any good ideas how to do it
class map:
	def __init__(self,rsWindow,areaMapPath):
		self.rsw = rsWindow
		self.mapPath = areaMapPath
		self.mapImg = PIL.Image.open(areaMapPath)
		self.mapImgGs = self.mapImg.convert("L")
	