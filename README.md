# x86-img-viewer
A basic image viewer written in Assembly to display an image through Dos on x86 architechture. Requires conversion to supported file format using the supplied python script.
  
imgflat python scripts take inimg.jpg(located in same folder, no args for now) as input and outputs a file named img.

imgflat script is available in dither and non dither versions along with the ability to use Multi-processing by breaking up the image into 4 parts processed on 4 seperate processes.

This img file is taken as an input by imgview.COM, it also supports auto centring, those black bars on the edges are not prerendered by imgflat script, IT IS CENTERED using asm code. :)
