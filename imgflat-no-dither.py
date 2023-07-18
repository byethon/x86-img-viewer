import cv2
import numpy as np
import os
imgfile=open(f"img","r+")
imgfile.seek(0,0)
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
imgfile.flush()
img= cv2.resize(imgsrc, (w,h), interpolation=cv2.INTER_AREA)
ratio = np.amax(img) / 2
img4 = (img / ratio).astype('uint8')
img4 = (img4*255).astype('uint8')
i=w-1
avgr=np.average(np.transpose(img4)[0])
avgg=np.average(np.transpose(img4)[1])
avgb=np.average(np.transpose(img4)[2])
print(f"{avgr},{avgg},{avgb}")
while(i!=0):
    j=h-1
    while(j!=0):
        k=0
        if(img4[j][i][0]):
            k+=1
        if(img4[j][i][1]):
            k+=2
        if(img4[j][i][2]):
            k+=4
        if(int(img4[j][i][0])>=avgr or int(img4[j][i][1])>=avgg or int(img4[j][i][2])>avgb):
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
        