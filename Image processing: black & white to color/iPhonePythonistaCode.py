# coding: utf-8
import numpy as np
import Image
import photos
import dialogs
import matplotlib.pyplot as mpl

def mapping(imcol,imbw1):
	mapp=np.ones((256,3),dtype='uint8')
	piximcol=imcol.load()
	piximbw1=imbw1.load()
	for i in range(imcol.size[0]):
		for j in range(imcol.size[1]):
			mapp[piximbw1[i,j],0]=piximcol[i,j][0]
			mapp[piximbw1[i,j],1]=piximcol[i,j][1]
			mapp[piximbw1[i,j],2]=piximcol[i,j][2]
	for i in range(mapp.shape[0]):
		for j in range(3):
			if mapp[i,j]==1:
				if i==255:
					mapp[i,j]=mapp[i-1,j]
				else:
					mapp[i,j]=max(mapp[i+1,j],mapp[i-1,j])
	return mapp
	
def colorize(imbw,mapp):
	imbwcol=Image.new('RGB',list(imbw.size))
	pixelbw=imbw.load()
	pixelcol=imbwcol.load()
	for i in range(imbw.size[0]):
		for j in range(imbw.size[1]):
			pixelcol[i,j]=tuple(mapp[pixelbw[i,j]])
	return imbwcol
	
def main():
	mode=dialogs.alert('Select the image','','Photos')
	if mode ==1:
		imbw=photos.pick_image()
		imbw=imbw.convert('L')
	type=dialogs.alert('Type of photo','','Landscape','Portrait')
	if type==1:
		imcolm=Image.open('test:Sailboat')
		imcolm=imcolm.convert('RGB')
		imbwm=imcolm.convert('L')
		imcolm=np.array(imcolm)
		imbw1=np.array(imbwm)

		imcolhalf2=np.ones((60,256,3))
		imcolhalf2[:,:,0]=imcolm[135:195,:,0]
		imcolhalf2[:,:,1]=imcolm[135:195,:,1]
		imcolhalf2[:,:,2]=imcolm[135:195,:,2]
		imcolhalf2=np.uint8(imcolhalf2)

		imbw1half2=imbw1[135:195,:]
		imcolhalf2=Image.fromarray(imcolhalf2,'RGB')
		imbw1half2=Image.fromarray(imbw1half2,'L')
		mapa=mapping(imcolhalf2,imbw1half2)
	elif type==2:
		imcolm=Image.open('test:Lenna')
		imcolm=imcolm.convert('RGB')
		imbwm=imcolm.convert('L')
		mapa=mapping(imcolm,imbwm)
	imbwcol=colorize(imbw,mapa)
	imbw.show()
	imbwcol.show()
main()
