# coding : utf-8
import sys,os,numpy
from PIL import Image

if len(sys.argv) == 1:
	print("Please input a image")
	quit()
try:
	Image.open(sys.argv[1])
except FileNotFoundError:
	print("Please input a valid image")
	quit()
except:
	print("Please report this bug")
	quit()

def round(a):
	return int(a+0.5)

def CMYK(list):
	if type(list) == type(1):
		return [100,100,100,100]
	if len(list) < 3:
		return [100,100,100,100]
	Rc = list[0] / 255
	Gc = list[1] / 255
	Bc = list[2] / 255
	K = 1 - max(Rc, Gc, Bc);
	C = (1 - Rc - K) / (1.01 - K)
	M = (1 - Gc - K) / (1.01 - K)
	Y = (1 - Bc - K) / (1.01 - K)
	return [C,M,Y,K]

def CmDistance(a,b):
	a = CMYK(a)
	b = CMYK(b)
	m = 0
	for i in range(4):
		m += (a[i]-b[i])**2
	return m

origin = sys.argv[1]
i = Image.open(origin)
m = i.size
i = i.resize((m[0],round(m[1]*1.136)))

# this 1.136 defines the vertical stretch of image, on wechat 1.136 is the best

wid = 12
scale = (wid) / i.size[0]
heit  = round(i.size[1] * scale / 4) * 4
i = i.resize((wid*4,heit*4))

fi = open("map","r",encoding="utf-8")
a = eval(fi.read())
output = open("out.txt","w",encoding="utf-8")

count = 0

for x in range(heit):
	for y in range(wid):
		target = numpy.asarray(i.crop((y*4,x*4,y*4+4,x*4+4))).tolist()
		smal_id = None
		smal_dis = None
		for n in a:
			q = 0
			for xi in range(4):
				for yi in range(4):
					if type(a[n][xi][yi]) == type(1) or len(a[n][xi][yi]) < 4:
						al = 1000
					else:
						k = a[n][xi][yi][3] / 255
						al = 1/(-k**2+2*k+0.01)
					q += CmDistance(a[n][xi][yi],target[xi][yi])*al
			if smal_dis == None or q < smal_dis:
				smal_id = n
				smal_dis = q
		output.write(smal_id)
		count += 1
		print("\r%s/%s"%(count,heit*wid),end="")
	output.write("\n")