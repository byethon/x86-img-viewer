import cv2
import numpy as np
import os
from multiprocessing import Process,Queue


def minmax(v):
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    return v

def crop_dither_gray(order,queue,inMat, samplingF,sr,er,sc,ec,osr,oer,osc,oec):
    inMat=inMat[sr:er,sc:ec]
    h = inMat.shape[0]
    w = inMat.shape[1]
    print(f"Process {order} : Floyd–Steinberg dithering in grayscale initiated")
    print(f"Process {order} : Image slice and dimensions set")
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
    print(f"Process {order} : Done! Image slice dithered!")
    inMat=inMat[0-osr:h-oer,0-osc:w-oec]
    print(f"Process {order} : Buffer margin cropped!")
    print(f"Process {order} : DONE!")
    queue.put([order,inMat])

def crop_dither_color(order,queue,inMat, samplingF,sr,er,sc,ec,osr,oer,osc,oec):
    inMat=inMat[sr:er,sc:ec]
    h = inMat.shape[0]
    w = inMat.shape[1]
    print(f"Process {order} : Floyd–Steinberg dithering in colour initiated")
    print(f"Process {order} : Image slice and dimensions set")
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
    print(f"Process {order} : Image slice dithered!")
    inMat=inMat[0-osr:h-oer,0-osc:w-oec]
    print(f"Process {order} : Buffer margin cropped!")
    print(f"Process {order} : DONE!")
    queue.put([order,inMat])

if __name__=='__main__':
    buf=5
    buf=int(buf)
    Q1=Queue()
    imgfile=open(f"img","r+")
    print("Output File Created")
    imgfile.seek(0,0)
    BaseDir = os.path.dirname(os.path.abspath(__file__))
    inimg = os.path.join(BaseDir, 'inimg.jpg')
    print("Input image received")
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
    print("Image dimensions finalized")
    img= cv2.resize(imgsrc, (w,h), interpolation=cv2.INTER_AREA)
    print("Image scaled")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("Auxilary grayscale image generated")
    print("Multi-Process sequence starting")
    p1 = Process(target = crop_dither_gray ,args=(0,Q1,gray,1,0,int(h/2)+buf,0,int(w/2)+buf,0,buf,0,buf))
    print("Process 1 : Loaded")
    p3 = Process(target = crop_dither_gray ,args=(1,Q1,gray,1,0,int(h/2)+buf,int(w/2)-buf,w,0,buf,-buf,0))
    print("Process 3 : Loaded")
    p5 = Process(target = crop_dither_gray ,args=(2,Q1,gray,1,int(h/2)-buf,h,0,int(w/2)+buf,-buf,0,0,buf))
    print("Process 5 : Loaded")
    p7 = Process(target = crop_dither_gray ,args=(3,Q1,gray,1,int(h/2)-buf,h,int(w/2)-buf,w,-buf,0,-buf,0))
    print("Process 7 : Loaded")
    p2 = Process(target = crop_dither_color,args=(4,Q1,img,1,0,int(h/2)+buf,0,int(w/2)+buf,0,buf,0,buf))
    print("Process 2 : Loaded")
    p4 = Process(target = crop_dither_color,args=(5,Q1,img,1,0,int(h/2)+buf,int(w/2)-buf,w,0,buf,-buf,0))
    print("Process 4 : Loaded")
    p6 = Process(target = crop_dither_color,args=(6,Q1,img,1,int(h/2)-buf,h,0,int(w/2)+buf,-buf,0,0,buf))
    print("Process 6 : Loaded")
    p8 = Process(target = crop_dither_color,args=(7,Q1,img,1,int(h/2)-buf,h,int(w/2)-buf,w,-buf,0,-buf,0))
    print("Process 8 : Loaded")
    p2.start()
    p4.start()
    p6.start()
    p8.start()
    p1.start()
    p3.start()
    p5.start()
    p7.start()
    outimg=[0,0,0,0,0,0,0,0]
    print("Dithered slice received")
    for i in range(8):
        k=Q1.get()
        outimg[k[0]]=k[1]
    print("Concatenating Image Slices")
    vs1=np.concatenate((outimg[0],outimg[2]),axis=0)
    vs2=np.concatenate((outimg[1],outimg[3]),axis=0)
    grayD=np.concatenate((vs1,vs2),axis=1)
    print("Auxilary Grayscale-Dithered Image recovered")
    vs1=np.concatenate((outimg[4],outimg[6]),axis=0)
    vs2=np.concatenate((outimg[5],outimg[7]),axis=0)
    colorD=np.concatenate((vs1,vs2),axis=1)
    print("Colour-Dithered Image recovered")
    print("Now starting file writing procedure")
    print("Output range set!")
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
    print("Output written successfully")
    print("Exiting Script")