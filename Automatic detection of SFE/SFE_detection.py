# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:03:41 2015

@author: gastoncrecikeinbaum
"""
import time 
import numpy as np
import pylab as pl
import ephem as ep
import csv
import os
import errno
    
Date=[]
Time1=[]
Time=[]
X=[]
Y=[]
Z=[]
F=[]
T=[]
X1=[]
Y1=[]
Z1=[]
F1=[]
a=[]
h=[]
anum=[]
X_e=[]
Y_e=[]
#Aqui tenim les funcions definides. El codi es troba més abaix.
#Definim
def param():
    Date=[]
    Time1=[]
    Time=[]
    X=[]
    Y=[]
    Z=[]
    F=[]
    T=[]
    X1=[]
    Y1=[]
    Z1=[]
    F1=[]
    a=[]
    h=[]
    anum=[]
    X_e=[]
    Y_e=[]
#Obrim l'arxiu .txt i decodifiquem les dades.
def Open_data(nom_arxiu):
    with open (nom_arxiu,'rb') as inputFile:
        lines = []
        for line in inputFile.readlines():
            lines.append(line)
    listarray=[] 
    for i in range(len(lines)):
        lineStripped = lines[i].strip()
        lineSplitted = lineStripped.split()
        listarray.append(lineSplitted)
    array=np.array(listarray)
    for k in array:
        b=k[0].isalpha()
        a.append(b)
    a.reverse()
    for i in a:
        anum.append(-i)
    i=0
    while anum[i] == 0:
        h.append(1)
        i=i+1
    difindex=len(a)-len(h)
    del lines[0:difindex]
    for i in range(len(lines)):
        lineStripped = lines[i].strip() 
        lineSplitted = lineStripped.split()
        Time1.append((lineSplitted[1]))
        Date.append((lineSplitted[0]))
        X1.append(float(lineSplitted[3]))
        Y1.append(float(lineSplitted[4]))
        Z1.append(float(lineSplitted[5]))
        F1.append(float(lineSplitted[6]))
    for i in Time1:
        t=time.strptime(i, "%H:%M:%S.000")
        b=(float(t[3])+(float(t[4])/60))
        Time.append(b)
    A=np.column_stack((X1,Y1,Z1,F1,Time)) #Fem un array amb les dades.
    A_array= extrapolation(A)
    Dades=A[np.all(A != 99999.0, axis=1)]
    for k in Dades: 
        X.append(float(k[0]))
        Y.append(float(k[1]))
        Z.append(float(k[2]))
        F.append(float(k[3]))
        T.append(float(k[4]))
    for n in A_array:
        X_e.append(float(n[0]))
        Y_e.append(float(n[1]))
    return X,Y,Z,F,T,Date,Time1,X_e,Y_e,Time

def Time_funct():
    hores=[]  
    minuts=[]
    hores_minuts=[]
    Time=[]
    Time_str=[]
    for h in range(24):
        hores.append(h)
    for n,h in enumerate(range(1440)):
        hores_minuts.append(float(n/60))
    for h in hores:
        for i in range(60):
            minuts.append(float(i))
    for h,m in zip(hores_minuts,minuts):
        Time.append(h+m/60)
    for h in hores:
        for i in range(60):
            if 0<=i<10:
                str_time=str(int(h))+':0'+str(int(minuts[i]))+':'+'00.000'
            else:
                str_time=str(int(h))+':'+str(int(minuts[i]))+':'+'00.000'
            Time_str.append(str_time)
    return Time,Time_str
    
def extrapolation(A): #This function replaces the 99999.0 for an extrapolation. 
    #A_list=[]
    for num,lista in enumerate(A):
    #for j in index_lista:        
        #if lista[j] == 99999.0:
        for k,i in enumerate(lista):
            if i == 99999.0:
                if A[num+1][k] == 99999.0:
                    A[num][k]=A[num-1][k]
                elif A[num][k] == 99999.0:
                    A[num][k]=(A[num+1][k])
                elif A[num][k] and A[num+1][k] == 99999.0:
                    cont1=1
                    b=num+cont1
                    cont2=-1 
                    f=num+cont2               
                    while True:
                        if A[b][k]==99999.0:
                            cont1=cont1+1
                        elif A[f][k]==99999.0:
                            cont2=cont2-1
                        elif A[b][k] and A[f][k]!=99999.0:
                            break
                    A[num][k]=((A[b][k]+A[f][k])/2)
                else:
                    A[num][k]=((A[num-1][k]+A[num+1][k])/2)
            #elif i != 99999.0:
             #   A_list.append(i)
    return A

#Fem la representació gràfica.
def Plot_data(X,Y,Z,F,T,title,ax1label,ax2label,ax3label,ax4label):
    f, (ax1, ax2, ax3, ax4) = pl.subplots(4, sharex=True, sharey=False) #Fem que comparteixin l'eix temporal.
    ax1.plot(T, X)
    ax1.set_title(title)
    ax1.set_ylabel(ax1label)
    ax2.plot(T,Y)
    ax2.set_ylabel(ax2label)
    ax3.plot(T,Z)
    ax3.set_ylabel(ax3label)
    ax4.plot(T,F)
    ax4.set_ylabel(ax4label)
    pl.xlabel('Universal Time (Hour)')
    f.subplots_adjust(hspace=0.2) #Ajustem la separació vertical entre subplots
    pl.xticks([3*k for k in range(0,9)],['00','03','06','09','12','15','18','21','00']) #etiquetem les dades
    pl.xlim(0,24) #quadrem l'eix entre 0 i 24.
    pl.show()
#Esborrem totes les llistes que hem fet servir.
def clear():
    del X[:]
    del Y[:]
    del Z[:]
    del F[:]
    del T[:]
    del Time1[:]
    del Time[:]
    del X1[:]
    del Z1[:]
    del Y1[:]
    del F1[:]
    del a[:]
    del anum[:]
    del h[:]
    del Date[:]
    del X_e[:]
    del Y_e[:]
def magnetograma(X,Y,Z,F,T,NamesObs_str,num):
    Plot_data(X,Y,Z,F,T,'Magnetograma '+NamesObs_str[num],'X (nT)','Y (nT)','Z (nT)','F (nT)')
def derivate(X,Y,T):
    minutes=[]
    for i in T:
        minutes.append(i*60)
    Tg=T[1:]
    DX=np.diff(X)/np.diff(minutes)
    DY=np.diff(Y)/np.diff(minutes)
    return DX,DY,Tg
def subsolar_point(Date,Timefloat):
    Dateslash=[]    
    s=ep.Sun()
    longitude_solar=[]
    declination_solar=[]
    greenwich = ep.Observer()
    greenwich.lat = '51:28:38'
    for i in range(len(Timefloat)):
        Dateslash.append(Date)
    for d,t in zip(Dateslash,Timefloat):
        k=d+' '+t
        greenwich.date=(k)
        s.compute(k)
        sdec=ep.degrees(s.dec)
        lon = s.ra - greenwich.sidereal_time()
        lonn=ep.degrees(lon)
        longitude_solar.append(ep.degrees(lonn.norm))
        declination_solar.append(sdec.norm)
    return longitude_solar, declination_solar
def Observat(Carpeta1):
    import csv
    Colatitudestr=[]
    Eastlongitudestr=[]
    colatitude=[]
    eastlongitude=[]
    NamesObs1=[]
    nomarxiu=Carpeta1+'/'+'/Observatories.csv'
    with open(nomarxiu, 'rbU') as csvfile:
        File = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in File:
            NamesObs1.append(row[0])
            Colatitudestr.append(row[3])
            Eastlongitudestr.append(row[4])
    NamesObs=NamesObs1[1:]
    Colatitudenum=Colatitudestr[1:]
    Eastlongitudenum=Eastlongitudestr[1:]
    for c,e in zip(Colatitudenum,Eastlongitudenum):
        LineStripped=c.strip('\xc2\xb0')
        LineStripped1=e.strip('\xc2\xb0')
        colatitude.append(float(LineStripped))
        eastlongitude.append(float(LineStripped1))
    return colatitude, eastlongitude, NamesObs
def arguments(Date,Timefloat,Carpeta1):    
    colatitude, eastlongitude,NamesObs=Observat(Carpeta1)
    longitude_solar, declination_solar=subsolar_point(Date, Timefloat)
    colatitude_rad=[]
    for i in colatitude:
        b=i*np.pi/180
        colatitude_rad.append(b)
    colatitude_solar=[]
    for i in declination_solar:
        colatitude_solar.append((np.pi/2)-i)
    #Ara hem passat tot a colatitud amb un argument entre [0,π]
    #Farem el mateix amb la longitud dels observatoris.
    longitude_rad1=[]
    longitude_rad=[]
    for i in eastlongitude:
        b=i*np.pi/180
        longitude_rad1.append(b)
    for i in range(len(longitude_rad1)): #Arreglem els arguments ja que hi han números que són més grans en mòdul que π
        if longitude_rad1[i] > np.pi:
            longitude_rad.append(longitude_rad1[i]-2*np.pi)
        elif longitude_rad1[i] < -np.pi:
            longitude_rad.append(longitude_rad1[i]+2*np.pi)
        else:
            longitude_rad.append(longitude_rad1[i])
    return longitude_rad,colatitude_rad,colatitude_solar,NamesObs
    
def rotation(phi_pss,longitude,colatitude,longitude_solar):
    M_rot=np.matrix( [[1,0,0], [0,np.cos(phi_pss),-np.sin(phi_pss)], [0,np.sin(phi_pss),np.cos(phi_pss)]] )
    coord_eq=np.array([[np.sin(longitude_solar-longitude)*np.sin(colatitude)],[np.cos(longitude_solar-longitude)*np.sin(colatitude)],[np.cos(colatitude)]])
    coord_subsolar=M_rot*coord_eq
    phi_ss=np.arctan2(coord_subsolar[1],coord_subsolar[0])
    chi_ss=np.arccos(coord_subsolar[2])
    return float(phi_ss),float(chi_ss)
    
def coord_change(Date_str,Date,Timefloat,Carpeta1):
    sfe_focus_colat,sfe_focus_long=focus_sfe(Date_str,Date,Timefloat,Carpeta1)
    longitude_rad,colatitude_rad,colatitude_solar,NamesObs=arguments(Date,Timefloat,Carpeta1)
    phi_sfe=[]
    chi_sfe=[]
    for cr,lr in zip(colatitude_rad,longitude_rad):
        for k,m in zip(sfe_focus_colat,sfe_focus_long):#Apliquem la rotació per cada posicíó del focus i observatori.
            phi_ss,chi_ss=rotation(k,lr,cr,m)
            phi_sfe.append(phi_ss)
            chi_sfe.append(chi_ss)
    #Ara tenim una llista on els primers 1440 elements són els de cada observatori.
    #Per tant farem un array de dimensions 144 (observatoris) x 1440 de manera
    #que tindrem cada observatori a cada fila i les seves corresponents dades indexades
    #segons la hora.
    colat_sfe_array=np.array(chi_sfe).reshape(144,1440)
    longit_sfe_array=np.array(phi_sfe).reshape(144,1440)
    return colat_sfe_array, longit_sfe_array,NamesObs,sfe_focus_colat,sfe_focus_long
    
def focus_sfe(Date,Date_str,Timefloat,Carpeta1):
    longitude_solar, declination_solar=subsolar_point(Date_str,Timefloat)
    longitude_rad,colatitude_rad,colatitude_solar,NamesObs=arguments(Date_str,Timefloat,Carpeta1)
    month=float(Date[1])
    Meses_array=np.array([[11,12,1,2],[5,6,7,8,9],[3,4,10]])
    for k,i in enumerate(Meses_array):
        for j in i:
            if j == month:
                if k == 0:
                    epoch = 'Hivern'
                elif k == 1:
                    epoch = 'Estiu'
                elif k == 2:
                    epoch = 'Equinoccis'
    if epoch == 'Hivern':
        latitude_sfe=(37/180)*np.pi #Passem de graus a radians
        colatitude_sfe=np.pi/2 - latitude_sfe #Passem a colatitud en radians
        longitude_sfe=(-12.6/180)*np.pi #Passem de graus a radians
    elif epoch == 'Estiu':
        latitude_sfe=(43.1/180)*np.pi 
        colatitude_sfe=np.pi/2 - latitude_sfe 
        longitude_sfe=(-4.6/180)*np.pi 
    elif epoch == 'Equinoccis':
        latitude_sfe=(42/180)*np.pi 
        colatitude_sfe=np.pi/2 - latitude_sfe 
        longitude_sfe=(-2/180)*np.pi
    longitude_subsolar_12UT, colatitude_subsolar_12UT = zip(longitude_solar,colatitude_solar)[720]
    longitude_resta=longitude_sfe-longitude_subsolar_12UT
    colatitude_resta= colatitude_subsolar_12UT-colatitude_sfe
    #Creem les noves coordenades del focus del sfe.
    sfe_focus_long=[]
    sfe_focus_long1=[]
    sfe_focus_colat=[]
    sfe_focus_colat1=[]
    for i in range(len(longitude_solar)):
        sfe_focus_long1.append(longitude_solar[i]-longitude_resta)
        sfe_focus_colat1.append(colatitude_solar[i]-colatitude_resta)
    for i in range(len(sfe_focus_long1)): #Arreglem els arguments ja que hi han números que són més grans en mòdul que π
        if sfe_focus_long1[i] > np.pi:
            sfe_focus_long.append(sfe_focus_long1[i]-2*np.pi)
        elif sfe_focus_long1[i] < -np.pi:
            sfe_focus_long.append(sfe_focus_long1[i]+2*np.pi)
        else:
            sfe_focus_long.append(sfe_focus_long1[i])
        if sfe_focus_colat1[i] > 2*np.pi:
            sfe_focus_colat.append(2*np.pi-sfe_focus_colat1[i])
        else:
            sfe_focus_colat.append(sfe_focus_colat1[i])
    return sfe_focus_colat, sfe_focus_long
def rang_colat(position,colat_sfe_array,NamesObs,rang_colat_min,rang_colat_max):
    nums=[]
    obs_names=[]
    if position >= 900:
        rang_colat_max1=40*np.pi/180
        rang_colat_min1=20*np.pi/180
    else:
        rang_colat_min1=rang_colat_min
        rang_colat_max1=rang_colat_max
    for k,i in enumerate(colat_sfe_array):
        if rang_colat_min1 <= i[position] <= rang_colat_max1:
            nums.append(k)
    for i in nums:
        obs_names.append(NamesObs[i])
    return nums,obs_names
    
def rang_colat_long_eq(position,colat_sfe_array,NamesObs,Time_str,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1):
    longitude_rad,colatitude_rad,colatitude_solar,NamesObs=arguments(Date_str,Time_str,Carpeta1)
    nums,obs_names=rang_colat(position,colat_sfe_array,NamesObs,rang_colat_min,rang_colat_max)
    delta=rang_colat_min
    obs_sfe_colat=[]
    obs_sfe_long=[]
    N_sfe=[]
    S_sfe=[]
    E_sfe=[]
    W_sfe=[]
    if position >= 900:
        deltaEW=20*np.pi/180
        deltaNS=20*np.pi/180
    else:
        deltaEW=delta
        deltaNS=delta
    for i in nums:
        obs_sfe_colat.append(colatitude_rad[i])
        obs_sfe_long.append(longitude_rad[i])
    for c,l,n in zip(obs_sfe_colat,obs_sfe_long,nums):
        if sfe_focus_colat[position]-deltaNS < c < sfe_focus_colat[position]+deltaNS:
            if l > sfe_focus_long[position]+deltaEW:
                E_sfe.append(n)
            elif l < sfe_focus_long[position]-deltaEW:
                W_sfe.append(n)
        if sfe_focus_long[position]-deltaNS < l < sfe_focus_long[position]+deltaNS:
            if c > sfe_focus_colat[position]+deltaNS:
                S_sfe.append(n)
            elif c < sfe_focus_colat[position]-deltaNS:
                N_sfe.append(n)
    return  N_sfe, S_sfe, E_sfe, W_sfe
def namesobs(NamesObs):
    NamesObs_minus=[]
    NamesObs_str=[]
    for i in NamesObs:
        nameobs=i.strip()
        nameobs_w=nameobs.strip('*')
        NamesObs_str.append(nameobs_w)
    for i in NamesObs_str:
        NamesObs_minus.append(i.lower())
    return NamesObs_minus,NamesObs_str
def Suma_obs(num,Date_file,Carpeta,NamesObs):
    NamesObs_minus,NamesObs_str=namesobs(NamesObs)
    letra=['d','v','p','q']
    letra_num=0
    while True:
        nom_arxiu=Carpeta+'/'+NamesObs_minus[num]+str(Date_file)+str(letra[letra_num])+'min.min'
        try:
            X,Y,Z,F,T,Date,Time1,X_e,Y_e,Time2=Open_data(nom_arxiu)
            break
        except IOError:
            letra_num=letra_num+1
    DX,DY,Tg=derivate(X_e,Y_e,Time2)
    return DX,DY,Tg
    
def SFE_set(Date_file,Carpeta,Time,Time_str,colat_sfe_array, NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1):
    SFE_time1=[]
    SFE_time2=[]
    SFE_time=[]  
    SFE_n1=[]
    SFE_n2=[]
    SFE_n=[]
    Total_list2=[]
    Total_list1=[]
    Total_list=[]
    for n,i in enumerate(Time):
        NamesObs_minus,NamesObs_str=namesobs(NamesObs)
        N_DX=[]
        S_DX=[]
        E_DY=[]
        W_DY=[]
        N_sfe, S_sfe, E_sfe, W_sfe=rang_colat_long_eq(n,colat_sfe_array,NamesObs,Time_str,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)
        for N in N_sfe:
            clear()
            try:
                DX,DY,Tg=Suma_obs(N,Date_file,Carpeta,NamesObs)
                N_DX.append(DX)
            except:
                pass
        for S in S_sfe:
            clear()
            try:
                DX,DY,Tg=Suma_obs(S,Date_file,Carpeta,NamesObs)
                S_DX.append(DX)
            except:
                pass
        for E in E_sfe:
            clear()
            try:
                DX,DY,Tg=Suma_obs(E,Date_file,Carpeta,NamesObs)
                E_DY.append(DY)
            except:
                pass
        for W in W_sfe:
            clear()
            try:
                DX,DY,Tg=Suma_obs(W,Date_file,Carpeta,NamesObs)
                W_DY.append(DY)
            except:
                pass
        E_sfe_suma1=sum(E_DY)
        try:
            E_sfe_suma=E_sfe_suma1/len(E_DY)
        except:
            E_sfe_suma=0
        W_sfe_suma1=sum(W_DY)
        try:
            W_sfe_suma=W_sfe_suma1/len(W_DY)
        except:
            W_sfe_suma=0
        EW=-E_sfe_suma+W_sfe_suma
        N_sfe_suma1=sum(N_DX)
        try:
            N_sfe_suma=N_sfe_suma1/len(N_DX)
        except:
            N_sfe_suma=0
        S_sfe_suma1=sum(S_DX)
        try:
            S_sfe_suma=S_sfe_suma1/len(S_DX)
        except:
            S_sfe_suma=0
        NS=-N_sfe_suma+S_sfe_suma
        
        Total=(EW+NS)/4#(len(E_DY)+len(W_DY)+len(N_DX)+len(S_DX))   
        Tg=Time[1:]
        deltatime=60        
        print str(float(n*100)/len(Time))[:5]+'% of the day '+str(Date_str)+'\r',

        if 1379>n>=60:#Això ho faig perque a cada temps només m'he de fixat en la
        #part de la delta que necessito.
            try:
                Range_deriv=Total[n-1-deltatime:n-1+deltatime]
                for l,i in enumerate(Range_deriv):
                    if i >= 1:
                        SFE_time1.append(l+n-1-deltatime)
                        SFE_n1.append(n)
                        Total_list1.append(Total)
            except:
                pass
        elif n <60:
            try:
                Range_deriv=Total[0:n-1+deltatime]
                for l,i in enumerate(Range_deriv):
                    if i >= 1:
                        SFE_time1.append(l)
                        SFE_n1.append(n)
                        Total_list1.append(Total)
            except:
                pass
        elif n>=1379:
            try:
                Range_deriv=Total[n-1-deltatime:1439]
                for l,i in enumerate(Range_deriv):
                    if i >= 1:
                        SFE_time1.append(l+n-1-deltatime)
                        SFE_n1.append(n)
                        Total_list1.append(Total)
            except:
                pass
        
    for n,i in enumerate(SFE_time1): #Per no tenir temps repetits
        if len(SFE_time1) == 1:
            SFE_time2.append(i)
            SFE_n2.append(SFE_n1[n])
            Total_list2.append(Total_list1[n])
        else:
            try:
                if i!=SFE_time1[n+1]:
                    SFE_time2.append(i) 
                    SFE_n2.append(SFE_n1[n])
                    Total_list2.append(Total_list1[n])
            except:
                pass
    for k,n in enumerate(SFE_n2):
        if len(SFE_n2)==1:
            SFE_n.append(n)
            SFE_time.append(SFE_time2[k])
            Total_list.append(Total_list2[k])
        else:
            try:
                if SFE_n2[k+1] > n+30:
                    SFE_n.append(n)
                    SFE_time.append(SFE_time2[k])
                    Total_list.append(Total_list2[k])
            except:
                pass  
    return SFE_time, SFE_n,Total_list,deltatime, Tg

def SFE_magnetograma(n,Date_file,Carpeta,Time,Time_str,colat_sfe_array, NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1):
    NamesObs_minus,NamesObs_str=namesobs(NamesObs)
    N_sfe, S_sfe, E_sfe, W_sfe=rang_colat_long_eq(n,colat_sfe_array,NamesObs,Time_str,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)
    for N in N_sfe:
        clear()
        try:
            Suma_magnetograma(N,Date_file,Carpeta,NamesObs)
        except:
            print 'No data from '+NamesObs_str[N]+' observatory'
    for S in S_sfe:
        clear()
        try:
            Suma_magnetograma(S,Date_file,Carpeta,NamesObs)
        except:
            print 'No data from '+NamesObs_str[S]+' observatory'
    for E in E_sfe:
        clear()
        try:
            Suma_magnetograma(E,Date_file,Carpeta,NamesObs)
        except:
            print 'No data from '+NamesObs_str[E]+' observatory'
    for W in W_sfe:
        clear()
        try:
            Suma_magnetograma(W,Date_file,Carpeta,NamesObs)
            
        except:
            print 'No data from '+NamesObs_str[W]+' observatory'
            
def Suma_magnetograma(num,Date_file,Carpeta,NamesObs):
    NamesObs_minus,NamesObs_str=namesobs(NamesObs)
    letra=['d','v','p','q']
    letra_num=0
    while True:
        nom_arxiu=Carpeta+'/'+NamesObs_minus[num]+str(Date_file)+str(letra[letra_num])+'min.min'
        try:
            X,Y,Z,F,T,Date,Time1,X_e,Y_e,Time2=Open_data(nom_arxiu)
            break
        except IOError:
            letra_num=letra_num+1
    print 'Observatori: ',NamesObs_str[num]
    magnetograma(X,Y,Z,F,T,NamesObs_str,num)
def writer(nomarxiu,Tg,enterdata,Date_str_time,Data_directory):
    with open(str(Data_directory)+'/'+str(nomarxiu)+".csv",'wb') as csvfile:
        writer=csv.writer(csvfile, delimiter=';',quotechar=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Time(hours)','Delta'])
        rows=zip(Tg,enterdata)
        for row in rows:
            writer.writerow(row)
#%%PROGRAMA#---------------------------------------------------------------------------------------------
def year():
    SFE_y=[]
    day_y=[]
    month_y=[]
    date_str_time=[]
    Data_directory=raw_input("Introduce the directory where you want to save the data folders: ")
    Carpeta1=raw_input("Introduce the directory of the 'Observatories.csv' file: ")
    Carpeta=raw_input("Introduce the directory of the Sfe's year files: ")
    year=raw_input("Introduce the year of the Sfe event (YYYY): ")
    months=range(1,13)
    days=range(1,32)
    rang_colat_min=(float(raw_input("Introduce the minimum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)
    rang_colat_max=(float(raw_input("Introduce the maximum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)        
    for month in months:
        for day in days:
            Date_str = str(day)+'/'+str(month)+'/'+str(year)
            try:
                Date_str_time1=time.strptime(Date_str, "%d/%m/%Y")
                date_str_time.append(Date_str_time1)
            except:
                pass  
    for Date_str_time in date_str_time:
        param()
        Time, Time_str=Time_funct()
        Date_file=int(Date_str_time[0])*10000+int(Date_str_time[1])*100+int(Date_str_time[2])     
        Date_str = str(Date_str_time[2])+'/'+str(Date_str_time[1])+'/'+str(Date_str_time[0])
        colat_sfe_array, longit_sfe_array, NamesObs,sfe_focus_colat,sfe_focus_long=coord_change(Date_str_time,Date_str,Time_str,Carpeta1) 
        SFE_time, SFE_n, Total_list, deltatime, Tg=SFE_set(Date_file,Carpeta,Time,Time_str,colat_sfe_array,NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)
        for i,n in zip(SFE_time,SFE_n):
            SFE_y.append(i)
            day_y.append(Date_str_time[2])
            month_y.append(Date_str_time[1])
        for total,n,i in zip(Total_list,SFE_n,SFE_time):
            try:
                os.makedirs(Data_directory+'/'+'Delta '+str(Date_str_time[0])+'/'+'Delta '+str(Date_str_time[1])+'/'+'Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/')
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            timesfe=time.strptime(Time_str[i], "%H:%M:%S.000")
            nomarxiu='Delta '+str(Date_str_time[0])+'/'+'Delta '+str(Date_str_time[1])+'/'+'Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/'+str(Date_str_time[2])+'-'+str(Date_str_time[1])+'-'+str(Date_str_time[0])+' '+str(timesfe[3])+'h'+str(timesfe[4])+'min'
            writer(nomarxiu,Tg,total,Date_str_time,Data_directory)
            #clear()
    for i,day,month in zip(SFE_y,day_y,month_y):    
        print 'SFE the day '+str(day)+'/'+str(month)+'/'+str(year)+' at '+Time_str[i]
          
def month():
    clear()
    SFE_m=[]
    day_m=[]
    date_str_time=[]       
    Data_directory=raw_input("Introduce the directory where you want to save the data folders: ")
    Carpeta1=raw_input("Introduce the directory of the 'Observatories.csv' file: ")
    Carpeta=raw_input("Introduce the directory of the Sfe's month files: ")
    year=raw_input("Introduce the year of the Sfe event (YYYY): ")
    month=raw_input("Introduce the month of the Sfe event (MM): ")
    days=range(1,32)
    rang_colat_min=(float(raw_input("Introduce the minimum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)
    rang_colat_max=(float(raw_input("Introduce the maximum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)        
    for day in days:
        Date_file=int(year)*10000+int(month)*100+int(day)     
        Date_str = str(day)+'/'+str(month)+'/'+str(year)
        try:
            Date_str_time1=time.strptime(Date_str, "%d/%m/%Y")
            date_str_time.append(Date_str_time1)
        except:
            pass    
    for Date_str_time in date_str_time:
        param()
        Time, Time_str=Time_funct()
        Date_file=int(Date_str_time[0])*10000+int(Date_str_time[1])*100+int(Date_str_time[2])     
        Date_str = str(Date_str_time[2])+'/'+str(Date_str_time[1])+'/'+str(Date_str_time[0])
        colat_sfe_array, longit_sfe_array, NamesObs,sfe_focus_colat,sfe_focus_long=coord_change(Date_str_time,Date_str,Time_str,Carpeta1) 
        SFE_time, SFE_n, Total_list, deltatime, Tg=SFE_set(Date_file,Carpeta,Time,Time_str,colat_sfe_array,NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)
        for i,n in zip(SFE_time,SFE_n):
            SFE_m.append(i)
            day_m.append(Date_str_time[2])
        for total,n,i in zip(Total_list,SFE_n,SFE_time):
            try:
                os.makedirs(Data_directory+'/'+'Delta '+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/'+'Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/')
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise 
            timesfe=time.strptime(Time_str[i], "%H:%M:%S.000")
            nomarxiu='Delta '+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/'+'Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/'+str(Date_str_time[2])+'-'+str(Date_str_time[1])+'-'+str(Date_str_time[0])+' '+str(timesfe[3])+'h'+str(timesfe[4])+'min'
            writer(nomarxiu,Tg,total,Date_str_time,Data_directory)
        #clear()
    for i,day in zip(SFE_m,day_m):    
        print 'SFE the day '+str(day)+'/'+str(month)+'/'+str(year)+' at '+Time_str[i]

def day():
    clear()
    param()
    Time, Time_str=Time_funct()
    Data_directory=raw_input("Introduce the directory where you want to save the data folders: ")
    Carpeta1=raw_input("Introduce the directory of the 'Observatories.csv' file: ")
    Carpeta = raw_input("Introduce the directory of the Sfe's day files: ")
    Date_str = raw_input("Introduce the date of the Sfe event (DD/MM/YYYY): ")
    Date_str_time=time.strptime(Date_str, "%d/%m/%Y")
    Date_file=Date_str_time[0]*10000+Date_str_time[1]*100+Date_str_time[2]
    rang_colat_min=(float(raw_input("Introduce the minimum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)
    rang_colat_max=(float(raw_input("Introduce the maximum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)        
    colat_sfe_array, longit_sfe_array, NamesObs,sfe_focus_colat,sfe_focus_long=coord_change(Date_str_time,Date_str,Time_str,Carpeta1) 
    SFE_time, SFE_n, Total_list, deltatime, Tg=SFE_set(Date_file,Carpeta,Time,Time_str,colat_sfe_array,NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)
    for i,n in zip(SFE_time,SFE_n):
        print 'SFE the day '+str(Date_str)+' at '+Time_str[i]
    for total,n,i in zip(Total_list,SFE_n,SFE_time):  
        timesfe=time.strptime(Time_str[i], "%H:%M:%S.000")
        try:
            os.makedirs(Data_directory+'/'+'Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise    
        nomarxiu='Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/'+str(Date_str_time[2])+'-'+str(Date_str_time[1])+'-'+str(Date_str_time[0])+' '+str(timesfe[3])+'h'+str(timesfe[4])+'min'
        writer(nomarxiu,Tg,total,Date_str_time,Data_directory)
    clear()

def day_magnetograma():
    clear()
    param()
    Time, Time_str=Time_funct()
    Data_directory=raw_input("Introduce the directory where you want to save the data folders: ")
    Carpeta1=raw_input("Introduce the directory of the 'Observatories.csv' file: ")
    Carpeta = raw_input("Introduce the directory of the Sfe's day files: ")
    Date_str = raw_input("Introduce the date of the Sfe event (DD/MM/YYYY): ")
    Date_str_time=time.strptime(Date_str, "%d/%m/%Y")
    Date_file=Date_str_time[0]*10000+Date_str_time[1]*100+Date_str_time[2]
    rang_colat_min=(float(raw_input("Introduce the minimum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)
    rang_colat_max=(float(raw_input("Introduce the maximum value of the colatitude range of the SFE focus (0º- +180º): ")))*(np.pi/180)        
    colat_sfe_array, longit_sfe_array, NamesObs,sfe_focus_colat,sfe_focus_long=coord_change(Date_str_time,Date_str,Time_str,Carpeta1) 
    SFE_time, SFE_n, Total_list, deltatime, Tg=SFE_set(Date_file,Carpeta,Time,Time_str,colat_sfe_array,NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)    
    for total,n,i in zip(Total_list,SFE_n,SFE_time):  
        timesfe=time.strptime(Time_str[i], "%H:%M:%S.000")
        pl.plot(Tg,total)
        try:
            os.makedirs(Data_directory+'/'+'Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        nomarxiu='Delta '+str(Date_str_time[2])+'_'+str(Date_str_time[1])+'_'+str(Date_str_time[0])+'/'+str(Date_str_time[2])+'-'+str(Date_str_time[1])+'-'+str(Date_str_time[0])+' '+str(timesfe[3])+'h'+str(timesfe[4])+'min'
        writer(nomarxiu,Tg,total,Date_str_time,Data_directory)
    pl.xlabel('Universal Time (Hour)')
    pl.xticks([3*k for k in range(0,9)],['00','03','06','09','12','15','18','21','00'])
    pl.xlim(0,24)
    pl.show()  
    for i,n in zip(SFE_time,SFE_n):
        print 'SFE the day '+str(Date_str)+' at '+Time_str[i]
        SFE_magnetograma(n,Date_file,Carpeta,Time,Time_str,colat_sfe_array,NamesObs,sfe_focus_colat,sfe_focus_long,Date_str,rang_colat_min,rang_colat_max,Carpeta1)
    clear()
#%%
def menu():
    print '-----------------------------------------------------------------------'
    print '                            SFE DETECTOR                               '
    print '-----------------------------------------------------------------------'
    print 'Select the period of time:                                             '
    print ' Day   - 1                                                             '
    print ' Month - 2                                                             '
    print ' Year  - 3                                                             '
    print '-----------------------------------------------------------------------'
    print 'If you want to see a specific day with the represented data - 4        '
    print '-----------------------------------------------------------------------'
    menu=int(raw_input('Introduce the option: '))
    while True:
        if menu == 1:
            day()
            break
        elif menu == 2:
            month()
            break
        elif menu == 3:
            year()
            break
        elif menu == 4:
            day_magnetograma()
            break
        else:
            print 'Introduce a valid number'
            menu=int(raw_input('Introduce the option: '))
    print '-----------------------------------------------------------------------'
    print 'Do you want to select another period (Y) or exit (another letter) ?    '
    print '-----------------------------------------------------------------------'
    YN=raw_input('Introduce the option: ')
    if YN == 'Y':
         print 'Select the period of time:                                             '
         print ' Day   - 1                                                             '
         print ' Month - 2                                                             '
         print ' Year  - 3                                                             '
         print '-----------------------------------------------------------------------'
         print 'If you want to see a specific day with the represented data - 4        '
         print '-----------------------------------------------------------------------'
         menu=int(raw_input('Introduce the option: '))
         while True:
             if menu == 1:
                 day()
                 break
             elif menu == 2:
                 month()
                 break
             elif menu == 3:
                 year()
                 break
             elif menu == 4:
                 day_magnetograma()
                 break
             else:
                 print 'Introduce a valid number'
                 menu=int(raw_input('Introduce the option: '))
    else:
        exit()
menu()