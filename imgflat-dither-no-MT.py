import cv2
import numpy as np
import os

def minmax(v):
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    return v

def dither_gray(inMat, samplingF):
    h = inMat.shape[0]
    w = inMat.shape[1]
    
    for y in range(0, h-1):
        for x in range(1, w-1):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
            inMat[y, x] = new_p
            
            quant_error_p = old_p - new_p
            
            inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 7 / 16.0)
            inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 3 / 16.0)
            inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 5 / 16.0)
            inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 1 / 16.0)
    return inMat

def dither_color(inMat, samplingF):
    h = inMat.shape[0]
    w = inMat.shape[1]
     
    for y in range(0, h-1):
        for x in range(1, w-1):
            old_b = inMat[y, x, 0]
            old_g = inMat[y, x, 1]
            old_r = inMat[y, x, 2]
            
            new_b = np.round(samplingF * old_b/255.0) * (255/samplingF)
            new_g = np.round(samplingF * old_g/255.0) * (255/samplingF)
            new_r = np.round(samplingF * old_r/255.0) * (255/samplingF)

            inMat[y, x, 0] = new_b
            inMat[y, x, 1] = new_g
            inMat[y, x, 2] = new_r

            quant_error_b = old_b - new_b
            quant_error_g = old_g - new_g
            quant_error_r = old_r - new_r

            inMat[y, x+1, 0] = minmax(inMat[y, x+1, 0] + quant_error_b * 7 / 16.0)
            inMat[y, x+1, 1] = minmax(inMat[y, x+1, 1] + quant_error_g * 7 / 16.0)
            inMat[y, x+1, 2] = minmax(inMat[y, x+1, 2] + quant_error_r * 7 / 16.0)
            
            inMat[y+1, x-1, 0] = minmax(inMat[y+1, x-1, 0] + quant_error_b * 3 / 16.0)
            inMat[y+1, x-1, 1] = minmax(inMat[y+1, x-1, 1] + quant_error_g * 3 / 16.0)
            inMat[y+1, x-1, 2] = minmax(inMat[y+1, x-1, 2] + quant_error_r * 3 / 16.0)

            inMat[y+1, x, 0] = minmax(inMat[y+1, x, 0] + quant_error_b * 5 / 16.0)
            inMat[y+1, x, 1] = minmax(inMat[y+1, x, 1] + quant_error_g * 5 / 16.0)
            inMat[y+1, x, 2] = minmax(inMat[y+1, x, 2] + quant_error_r * 5 / 16.0)

            inMat[y+1, x+1, 0] = minmax(inMat[y+1, x+1, 0] + quant_error_b * 1 / 16.0)
            inMat[y+1, x+1, 1] = minmax(inMat[y+1, x+1, 1] + quant_error_g * 1 / 16.0)
            inMat[y+1, x+1, 2] = minmax(inMat[y+1, x+1, 2] + quant_error_r * 1 / 16.0)
    return inMat

imgfile=open(f"img","w")
BaseDir = os.path.dirname(os.path.abspath(__file__))
inimg = os.path.join(BaseDir, 'inimg.jpg')
imgsrc = cv2.imread(inimg)
src_h, src_w, scr_c = imgsrc.shape
if(src_w/src_h>=640.0/480.0):
    w=640
    h=int(src_h/src_w*640)
if(src_w/src_h<640.0/480.0):
    w=int(src_w/src_h*480)
    h=480
if(h>=100 and w>=100):
    imgfile.write(f'{w}{h}')
if(h>=10 and h<100 and w>=100):
    imgfile.write(f'{w}0{h}')
if(h>=0 and h<10 and w>=100):
    imgfile.write(f'{w}00{h}')
if(w>=10 and w<100 and h>=100):
    imgfile.write(f'0{w}{h}')
if(w>=0 and w<10 and h>=100):
    imgfile.write(f'00{w}{h}')
img= cv2.resize(imgsrc, (w,h), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayD=dither_gray(gray,1)
colorD=dither_color(img,1)
i=w-1
while(i!=0):
    j=h-1
    while(j!=0):
        k=0
        if(colorD[j][i][0]):
            k+=1
        if(colorD[j][i][1]):
            k+=2
        if(colorD[j][i][2]):
            k+=4
        if(int(grayD[j][i])>180):
            k+=8
        if(k<=9):
            imgfile.write(f'{k}')
        if(k==10):
            imgfile.write(':')
        if(k==11):
            imgfile.write(';')
        if(k==12):
            imgfile.write('<')
        if(k==13):
            imgfile.write('=')
        if(k==14):
            imgfile.write('>')
        if(k==15):
            imgfile.write('?')
        j-=1
    i-=1
        