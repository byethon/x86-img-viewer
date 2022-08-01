.model tiny
.486
.data
filename1 db 'img',0
buffer db 479 dup(0),'0'
imgh dw 0
imgw dw 0
hlimit dw 0
wlimit dw 0
buflim dw 0
setw dw 0
seth dw 0
.code
.startup
jmp prog
b1:
pop ax
mov buflim,ax
jmp b2

prog:
lea dx, filename1
mov ah,3dh
mov al,0h
int 21h
mov bx,ax

call readi
mov ax,0
lea si,buffer
lodsb
sub ax,30h
mov cl,100
mul cl
mov imgw,ax
mov ax,0
lodsb
sub ax,30h
mov cl,10
mul cl
add ax,imgw
mov imgw,ax
mov ax,0
lodsb
sub ax,30h
add ax,imgw
dec ax
mov imgw,ax
mov ax,639
sub ax,imgw
mov cl,2
div cl
mov ah,0
mov wlimit,ax
add ax,imgw
mov setw,ax

mov ax,0
lodsb
sub ax,30h
mov cl,100
mul cl
mov imgh,ax
mov ax,0
lodsb
sub ax,30h
mov cl,10
mul cl
add ax,imgh
mov imgh,ax
mov ax,0
lodsb
sub ax,30h
add ax,imgh
dec ax
mov imgh,ax
mov ax,479
sub ax,imgh
mov cl,2
div cl
mov ah,0
mov hlimit,ax
add ax,imgh
mov seth,ax

sub ax,hlimit
push ax
mov ax,imgh
cmp ax,256
jnl b1
pop ax
mov buflim,ax

b2:

mov ah,0h
mov al,12h
int 10h

mov cx,setw
l1:
mov dx,seth
call readl
lea si,buffer
l2:
lodsb
sub al,30h
call pix
dec dx
cmp dx,hlimit
jne l2
dec cx
cmp cx,wlimit
jne l1

call closef
call holds

mov ah,0h
mov al,03h
int 10h

mov ax, 4C00h
int 21h

pix proc near
	push bx
	mov bx,0
	mov ah,0ch
	int 10h
	pop bx
	ret
pix endp

readl proc near
	push ax
	push cx
	push dx
	mov cx,buflim
	lea dx,buffer
	mov ah,3fh
	int 21h
	pop dx
	pop cx
	pop ax
	ret
readl endp

readi proc near
	push ax
	push cx
	push dx
	mov cx,6
	lea dx,buffer
	mov ah,3fh
	int 21h
	pop dx
	pop cx
	pop ax
	ret
readi endp

holds proc near
	mov ah,07h
	h1:
	int 21h
	cmp al,'%'
	jnz h1
	mov ah,0h
	mov al,3h
	int 10h
	ret
holds endp

closef proc near
	mov ah,3eh
	int 21h
	ret
closef endp

.exit
end
