#!/usr/bin/env python


import binascii
import sys

stacks = {"esp":[],"esi":[],"edi":[],"ebp":[]}
regs = ["eax","ecx","edx","ebx","esp","ebp","esi","edi","rt0","r9","r10","r11","r12","r13","r14"]
def get_op1(rA,rB,imm,icd):
   if icd == 3:
       return imm
   elif icd == 5:
       return '['+regs[rB]+']'
   elif icd in [2,6]:
       return regs[rA]
   elif icd == 8:
       return imm
   elif icd == 9:
       print(rB)
       return hex(stacks[regs[rB]][-1])
   elif icd == 10:
       return hex(int(input(),16))
   else:
       return "??"
def get_op2(rA,rB,imm,icd):
    if icd in [2,3]:
        return regs[rB]
    elif icd == 5:
        return regs[rA]
    elif icd == 6:
        return regs[rB]
    elif icd == 8:
        return regs[rB]
    elif icd == 9:
        return regs[rB]
    elif icd == 10:
        return regs[rB]
    elif icd == 7:
        return imm
    else:
        return "??"

def get_pc(pc,imm,icd,rB):
    if icd == 8 :
        stacks[regs[rB]].append(pc + 5)
        return int(imm,16)
    elif pc == 0xb8 :
        return pc + 1
    elif icd == 9:
        return stacks[regs[rB]].pop()
    elif icd == 10 :
        stacks[regs[rB]].append(pc + 5)
        return pc + 1
    elif icd in [0,12,13,14,15]:
        return pc
    elif icd in [1,2,6,10,11]:
        return pc + 1
    elif icd in [3,4,5,7,8]:
        return pc + 5
def get_men(icd,ifn):
    if icd in [2,3,5] :
        return "mov"
    elif icd == 6:
        if ifn == 0:
            return "add"
        if ifn == 1:
            return "sub"
        if ifn == 2:
            return "and"
        if ifn == 3:
            return "xor"
        if ifn == 4:
            return "mul"
        if ifn == 5:
            return "div"
        if ifn == 6:
            return "rem"
        if ifn == 7:
            return "sl"
        if ifn == 8:
            return "sr"
    elif icd == 7 :
        if ifn == 0 :
            return "b"
        if ifn == 4:
            return "bnq"
    elif icd == 8 :
        return "call"
    elif icd == 9:
        return f"ret"
    elif icd == 10:
        return "call"
    else:
        return "???"


f = open('flag-checker-v5.bin')
data = f.read()
data = data.replace(' ', '')
data = data[8:]

arr = bytearray.fromhex(data)
inst = [arr[x:x+10] for x in range(0,len(arr),10)]
pc = 0
while pc != 0x84:
   # for x in range(len(i)):
    #    print(f"byte {x} == {hex(i[x])}")
    i = arr[pc*2:pc*2+10]
    icd = (i[0] & 0xf0) >> 4
    ifn = i[0] & 0x0f
    imm = binascii.hexlify(i[2:])
    rA  = (i[1] & 0xf0) >> 4
    rB  = i[1] & 0x0f
    if sys.argv[1] == 'v' :
        print(f"Instruction = {binascii.hexlify(i)} pc = {hex(pc):^4} icd = {icd:^3} Ifn = {ifn:^3} imm = {imm} rA = {rA:^3} rB = {rB:^3}")
    men = get_men(icd,ifn)
    op1 = get_op1(rA,rB,imm,icd)
    op2 = get_op2(rA,rB,imm,icd)
   #print(sys.argv)
    print(f" {hex(pc)}: {men}  {op2},{op1},...")
    pc = get_pc(pc,imm,icd,rB)
