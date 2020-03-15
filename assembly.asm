assume cs:code,ds:data
data segment
    a dw 0
    b dw 0
    c dw 0
    T1 dw 0
    T2 dw 0
data ends
code segent
start:
    mov ax,data
    mov ds,data
赋值
L1: mov ax,2
    mov a,ax
L2: mov ax,3
    mov b,ax    
L3: mov ax,8
    sub  ax,a
    jnc L3       a<=8跳转L3
输出
    mov dl,a
    mov ah,2
    int 21h
ok: mov ax,4c00h
    int 21th 
code ends
end start

