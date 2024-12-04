# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 18:23:47 2016

@author: gastoncrecikeinbaum
"""
import matplotlib.pyplot as mpl
import numpy as np
import skimage.data

def mapping(imcol,imbw1): #Creació del mapa a partir de la imatge referència
    mapp=np.ones((256,3),dtype='uint8')
    for i in range(imcol.shape[0]):
        for j in range(imcol.shape[1]):
            mapp[imbw1[i,j],0]=imcol[i,j,0] #S'assigna a cada intensitat (posició de
            mapp[imbw1[i,j],1]=imcol[i,j,1] # la llista) un conjunt de valors RGB 
            mapp[imbw1[i,j],2]=imcol[i,j,2]       
    for i in range(mapp.shape[0]): #Procés d'extrapolació
        for j in range(3):
            if mapp[i,j]==1:
                if i == 255: #Es té en compte l'última posició
                    mapp[i,j]=mapp[i-1,j]
                else:
                    mapp[i,j]=max(mapp[i+1,j],mapp[i-1,j])            
    return mapp
    
def color(im,mapp): #Aplicació del mapa  
    imcol=np.ones((im.shape[0],im.shape[1],3),dtype='uint8')
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            imcol[i,j,0]=mapp[im[i,j],0]
            imcol[i,j,1]=mapp[im[i,j],1]
            imcol[i,j,2]=mapp[im[i,j],2]
    return imcol
    
def menu():
    print '-----------------------------------------------------------------------'
    print '                     BLACK AND WHITE TO COLOR                          '
    print '-----------------------------------------------------------------------'
    raw_input("Press any key to start")
    pathsipi=raw_input("Introduce the path of the SIPI library: ")
    print '-----------------------------------------------------------------------'
    path=raw_input("Introduce the path of the black and white image: ")
    print '-----------------------------------------------------------------------'
    imbw2=mpl.imread("/Users/gastoncrecikeinbaum/Downloads/IMG_4800.jpeg")
    try:
        imbw2=0.229*imbw2[:,:,0]+0.587*imbw2[:,:,1]+0.114*imbw2[:,:,2]
    except:
        pass
    print 'Select the type of photo                                               '
    print ' Landscape - 1                                                         '
    print ' Portrait  - 2                                                         '
    print '-----------------------------------------------------------------------'
    menu=int(raw_input("Introduce the option: "))
    if menu==1:
        imcol=mpl.imread(str(pathsipi)+"/4.2.06.tiff")
        imbw1=0.229*imcol[:,:,0]+0.587*imcol[:,:,1]+0.114*imcol[:,:,2]
        imcolhalf2=np.ones((140,512,3)) #Fem servir el mapa de la secció 2 (mirar treball)
        imcolhalf2[:,:,0]=imcol[250:390,:,0] #ja que és el més fotorealista.
        imcolhalf2[:,:,1]=imcol[250:390,:,1]
        imcolhalf2[:,:,2]=imcol[250:390,:,2]
        imcolhalf2=np.uint8(imcolhalf2)
        imbw1half2=imbw1[250:390,:]
        mapa=mapping(imcolhalf2,imbw1half2)
    elif menu==2:
        imcol=skimage.data.lena()
        imbw1=0.229*imcol[:,:,0]+0.587*imcol[:,:,1]+0.114*imcol[:,:,2]
        mapa=mapping(imcol,imbw1)        
    imconv=color(imbw2,mapa)
    mpl.figure()
    mpl.imshow(imconv)
menu()