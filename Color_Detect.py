import numpy as np
import cv2 as cv
import pandas as pd
import copy

image_name='colorpic.jpg'
image=cv.imread(image_name)
column_names=['colour','colour name','hex','r','g','b']
df=pd.read_csv('colors.csv',names=column_names,header=None)
image_copy=copy.deepcopy(image)
click=False
b=g=r=xpos=ypos=-1

def mouse_function(event,x,y,flag,params):
    global click,b,g,r,xpos,ypos,image,image_copy
    if event == cv.EVENT_LBUTTONDOWN:
        image_copy=copy.deepcopy(image)
        click=True
        b,g,r=image[y,x]
        b=int(b)
        g=int(g)
        r=int(r)
        xpos=x
        ypos=y

if image.shape[0]*image.shape[1]<=662000:
    cv.namedWindow('image')
else:
    cv.namedWindow('image',cv.WINDOW_NORMAL)

def Getcolorname(r,g,b):
    min=float('inf')
    for i in range(len(df)):
        distance= abs(df.loc[i,'r']-r) + abs(df.loc[i,'g']-g)+abs(df.loc[i,'b']-b)
        if distance < min:
            min=distance
            name=df.loc[i,'colour name']
    return name

while True:
    
    cv.imshow('image',image_copy)
    if click == True:
        cname=Getcolorname(r,g,b)
        
        #adjusting the size of the box where text will be put
        if(xpos>0.6*image.shape[1]):
            xpos=xpos-400
        else:
            xpos=xpos
        if (ypos<0.05*image.shape[0]):
            ypos=ypos+40
        else:
            ypos=ypos

        cv.rectangle(image_copy,(xpos,ypos-40),(xpos+600,ypos),(b,g,r),-1)
        text=cname+' R =' + str(r)+' G =' + str(g)+' B =' + str(b)
        
        #dark background light text
        if b+g+r>=600:
            cv.putText(image_copy, text,(xpos+10,ypos-10),2,0.6,(0,0,0),1,cv.LINE_AA)
        
        #light background dark text
        else: 
            cv.putText(image_copy,text,(xpos+10,ypos-10),2,0.6,(255,255,255),1,cv.LINE_AA)
    cv.setMouseCallback('image',mouse_function)
    
    k= cv.waitKey(20) & 0xFF 
    if k==27:       #exit on esc 
        break
    
cv.destroyAllWindows()

