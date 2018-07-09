# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 20:46:07 2017

@author: dmartin
"""

import numpy as np
import csv
import time
import sys

# Global variables

SolveThis=""
m=np.zeros((9,9,9), dtype=int)
sol=np.zeros((9,9), dtype=int)

show_detail=0

if sys.argv[1] != "":
    SolveThis=sys.argv[1]
    
#SolveThis="010000034000079500029300600030607420086100090000050000940205870800060200670084003"
#SolveThis="510070000039004507060800021073659080400230900006080700000912600000000003005000490"
#SolveThis="400000805030000000000700000020000060000080400000010000000603070500200000104000000"
#SolveThis="480300000000000071020000000705000060000200800000000000001076000300000400000050000"
#SolveThis="009078020030050800050019300060030200700090004005040080008720050002060090070980600"
#SolveThis="000027030400009500900540602000000004060000050200000000304071008006200001080390000"
#SolveThis="605027439400069507900543602000000004060000053200000006354671008796200341182394765"
#SolveThis="300080000000700005100000000000000360002004000070000000000060130045200000000000800"
#SolveThis="000002000000070001700300090800700000020890600013006000090050824000008910000000000"
#SolveThis="000658000004000000120000000000009607000300500002080003001900800306000004000047300"
#SolveThis="000658000004000000120000000000009607000370500002080003001900800306000004000047300"

#SolveThis="480300000000000071020000000705000060000200800000000000001076000300000400000050000"

# This one needs to find the pair in 6x8 and 6x9 of [5 7] to eliminate in rest of 3x3 square
SolveThis="100725439924863010000149286000586004000497003640231000790310002050670091001950008"


# Function definitions

def fill(r,c,val):
    sol[r,c]=val
    for i in range(0,9):
        sol[r][c]=val
        m[r, i, val-1]=1
        m[i, c, val-1]=1
        m[r/3*3+i/3, c/3*3+i%3, val-1]=1
        m[r,c,i]=1




def twin(r, c, dir, offset, val):
    change=0
    for i in range(0,9):
        if(dir=="col"):   # Fill column
            if(i/3 != r):
                if (m[i, c*3+offset, val]==0):
                    change=1
                m[i, c*3+offset, val]=1
        if(dir=="row"):   # Fill row
            if(i/3 != c):
                if (m[r*3+offset, i, val]==0):
                    change=1
                m[r*3+offset, i, val]=1
    return(change)




def eviltwin(r, c, dir, offset, val):
    change=0
    idx=range(0,9)
    if(dir=="col"):   # Fill column
        idx.remove(offset)
        idx.remove(offset+3)
        idx.remove(offset+6)
    if(dir=="row"):
        idx.remove(offset*3)
        idx.remove(offset*3+1)
        idx.remove(offset*3+2)
    for i in idx:
        if(m[r*3+i/3, c*3+i%3, val]==0):
            change=1
        m[r*3+i/3, c*3+i%3, val]=1
    return(change)
 
    
def identicaltwin(r, c, t1, t2, v1, v2):
    change=0
    for i in range(0,9):
        if i != t1 and i != t2:
            if m[r*3+i/3, c*3+i%3, v1]==0:
                change=1
                m[r*3+i/3, c*3+i%3, v1]=1
            if m[r*3+i/3, c*3+i%3, v2]==0:
                change=1
                m[r*3+i/3, c*3+i%3, v2]=1
    #detail_display()
    return(change)
    

def twistedtriplet(r, c, x, y, z, v1, v2, v3):
    change=0
    vals=range(0,9)
    vals.remove(v1)
    vals.remove(v2)
    vals.remove(v3)
    for i in (x, y, z):
        for val in vals:
            if(m[r*3+i/3, c*3+i%3, val]==0):
                change=1
            m[r*3+i/3, c*3+i%3, val]=1
    return(change)
            
 
 
def quadruplet(r, c, w, x, y, z, v1, v2, v3, v4):
    change=0
    vals=range(0,9)
    vals.remove(v1)
    vals.remove(v2)
    vals.remove(v3)
    vals.remove(v4)
    for i in (w, x, y, z):
        for val in vals:
            if(m[r*3+i/3, c*3+i%3, val]==0):
                change=1
            m[r*3+i/3, c*3+i%3, val]=1
    return(change)
 
 
 
def pairs(r, c, ia, ib, numa, numb):
    change=0
    # In index A and B, remove all other values
    vals=range(0,9)
    vals.remove(numa)
    vals.remove(numb)
    for v in vals:
        if(m[r*3+ia/3, c*3+ia%3, v]==0):
            change=1
            m[r*3+ia/3, c*3+ia%3, v]=1
            #print(" Marking",r+1,c+1,ia+1,i+1)
        if(m[r*3+ib/3, c*3+ib%3, v]==0):
            change=1
            m[r*3+ib/3, c*3+ib%3, v]=1
            #print(" Marking",r+1,c+1,ib+1,i+1)
#    # Also need to remove inverse values from remaining squares
#    idx=range(0,9)
#    idx.remove(ia)
#    idx.remove(ib)
#    for i in idx:
#        for v in (numa, numb):
#            if(m[r*3+ia/3, c*3+ia%3, v]==0):
#                #print "Changing %dx%d %d - %d" % (r+1,c+1,i+1,v+1)
#                next
#                #change=1
#                #m[r*3+ia/3, c*3+ia%3, v]=1
    return(change)
           



def display():
    for i in range(0,9):
        print(sol[i])
    if show_detail:
        detail_display()

def detail_display():
    for i in (range(0,9)):
        for j in (range(0,9)):
            if sum(m[i][j]) < 9:
                print "%dx%d = %s" % (i+1, j+1, np.where(m[i][j]==0)[0]+1)


def scan(debug=1):
    for x in range(0,9):   # step through each row and col
        for y in range(0,9):
            if (sol[x,y]==0):   # find empty squares
                if (sum(m[x,y])==8):
                    idx=np.where(m[x,y]==0)[0][0]+1   # locate index
                    fill(x,y,idx)
                    if (debug==1):
                        print "Found: %dx%d = %d" % (x+1,y+1,idx)
                        display()
                    return(1)
            for z in range(0,9):  # step through each number
                if (sum(m[0:9, y, z])==8):  # only number left in col
                    idx=np.where(m[0:9, y, z]==0)[0][0]
                    fill(idx,y,z+1)
                    if (debug==1):
                        print "Only num col: %dx%d = %d" % (idx+1,y+1,z+1)
                        display()
                    return(1)
                if (sum(m[x, 0:9, z])==8):  # only number left in row
                    idx=np.where(m[x, 0:9, z]==0)[0][0]
                    fill(x,idx,z+1)
                    if (debug==1):
                        print "Only num row: %dx%d = %d" % (x+1,idx+1,z+1)  
                        display()
                    return(1)
    # Scan each 3x3
    for x in range(0,3):
        for y in range(0,3):
            for z in range(0,9):   # scan through each number
                    mt=m[x*3:x*3+3, y*3:y*3+3, z]  # find missings
                    tmt=mt.reshape(1,9)[0]   # reshape to an array
                    if (sum(tmt)==8):
                        idx=np.where(tmt==0)[0][0]   # locate index
                        fill(x*3+idx/3, y*3+idx%3, z+1)
                        if (debug==1):
                            print "Only num square: %dx%d = %d" % (x*3+idx/3+1, y*3+idx%3+1, z+1)
                            display()
                        return(1)
    # Look for twins and triplets in each 3x3
    foundtwin=0
    for x in range(0,3):
        for y in range(0,3):
            for z in range(0,9):
                mt=m[x*3:x*3+3, y*3:y*3+3, z]  # find missings
                tmt=mt.reshape(1,9)[0]   # reshape to an array
                if (sum(tmt)==7):   # two missing values
                    idx=np.where(tmt==0)[0]
                    idxa=idx[0]
                    idxb=idx[1]
                    if (idxa/3 == idxb/3):
                        t=twin(x, y, "row", idxa/3, z)
                        if (debug==1 and t>0):
                            print("Twin sq row", x+1, y+1, idxa+1, idxb+1, z+1)
                        foundtwin+=t
                    if (idxa%3 == idxb%3):
                        t=twin(x, y, "col", idxa%3, z)
                        if (debug==1 and t>0):
                            print("Twin sq col", x+1, y+1, idxa+1, idxb+1, z+1)
                        foundtwin+=t
                    # Remove these values from other spots in 3x3 square
                if (sum(tmt)==6):   # three missing values
                    idx=np.where(tmt==0)[0]
                    idxa=idx[0]
                    idxb=idx[1]
                    idxc=idx[2]
                    if (idxa/3 == idxb/3 and idxa/3 == idxc/3):
                        t=twin(x, y, "row", idxa/3, z)
                        if (debug==1 and t>0):
                            print("Triplet sq row", x+1, y+1, idxa+1, idxb+1, idxc+1, z+1)
                        foundtwin+=t
                    if (idxa%3 == idxb%3 and idxa%3 == idxc%3):
                        t=twin(x, y, "col", idxa%3, z)
                        if (debug==1 and t>0):
                            print("Triplet sq col", x+1, y+1, idxa+1, idxb+1, idxc+1, z+1)
                        foundtwin+=t
                    # Remove these values from other spots in 3x3 square
    if(foundtwin>0):
        return(1)
    # Look for hidden twins                        
    for x in range(0,3):
        for y in range(0,3):
            for za in range(0,8):
                for zb in range(za+1,9):
                    if (za != zb):
                        mta=m[x*3:x*3+3, y*3:y*3+3, za]
                        tmta=mta.reshape(1,9)[0]
                        mtb=m[x*3:x*3+3, y*3:y*3+3, zb]
                        tmtb=mtb.reshape(1,9)[0]
                        if (sum(tmta)==7 and sum(tmtb)==7):
                            idxa=np.where(tmta==0)[0]
                            idxb=np.where(tmtb==0)[0]
                            if(sum(idxa==idxb)==2):
                                #print "Found possible pair: %dx%d %d %d = [%d %d]" % (x+1,y+1,idxa[0]+1,idxa[1]+1,za+1,zb+1)
                                t=pairs(x, y, idxa[0], idxa[1], za, zb)
                                if (debug==1 and t>0):
                                    print("Hidden twin", x+1, y+1, idxa+1, za+1, zb+1)
                                foundtwin+=t
    if(foundtwin>0):
        return(1)               
    # Look for evil twins
    for x in range(0,3):
        for ya in (0,1):
            for yb in range(ya+1,3):
                for z in range(0,9):
                    # First look at row of 3x3 squares
                    mta=m[x*3:x*3+3, ya*3:ya*3+3, z]
                    tmta=mta.reshape(1,9)[0]
                    mtb=m[x*3:x*3+3, yb*3:yb*3+3, z]
                    tmtb=mtb.reshape(1,9)[0]
                    if (sum(tmta)==7 and sum(tmtb)==7):
                        idxa=np.where(tmta==0)[0]
                        idxb=np.where(tmtb==0)[0]
                        if (idxa[0]/3 == idxb[0]/3 and idxa[1]/3 == idxb[1]/3 or
                            idxa[0]/3 == idxb[1]/3 and idxa[1]/3 == idxb[0]/3):
                            t=eviltwin(x, 3-ya-yb, "row", 3-idxa[0]/3-idxa[1]/3, z)
                            if (debug==1 and t>0):
                                print("Evil twin row", x+1, 3-ya-yb+1, 3-idxa[0]/3-idxa[1]/3+1, z+1)
                            foundtwin+=t
                    # Next look at col of 3x3 squares
                    mta=m[ya*3:ya*3+3, x*3:x*3+3, z]
                    tmta=mta.reshape(1,9)[0]
                    mtb=m[yb*3:yb*3+3, x*3:x*3+3, z]
                    tmtb=mtb.reshape(1,9)[0]
                    if (sum(tmta)==7 and sum(tmtb)==7):
                        idxa=np.where(tmta==0)[0]
                        idxb=np.where(tmtb==0)[0]
                        if (idxa[0]%3 == idxb[0]%3 and idxa[1]%3 == idxb[1]%3 or
                            idxa[0]%3 == idxb[1]%3 and idxa[1]%3 == idxb[0]%3):
                            t=eviltwin(3-ya-yb, x, "col", 3-idxa[0]%3-idxa[1]%3, z)
                            if (debug==1 and t>0):
                                print("Evil twin col", 3-ya-yb+1, x+1, 3-idxa[0]%3-idxa[1]%3+1, z+1)
                            foundtwin+=t
    if(foundtwin>0):
        return(foundtwin)

    # Look for identical twins
    for x in range(0,3):
        for y in range(0,3):
            for za in range(0,8):
                for zb in range(za+1,9):
                    i1 = x*3 + za/3
                    j1 = y*3 + za%3
                    i2 = x*3 + zb/3
                    j2 = y*3 + zb%3
                    w1 = np.where(m[i1][j1]==0)[0]
                    w2 = np.where(m[i2][j2]==0)[0]
                    if sum(m[i1][j1]) == 7 and sum(m[i2][j2]) == 7 and (w1 == w2).all():
                        w=np.where(m[i1][j1]==0)[0]
                        t=identicaltwin(x,y,za,zb,w[0],w[1])
                        if debug==1 and t>0:
                            print "Identical twins %dx%d and %dx%d = %s" % (i1+1, j1+1, i2+1, j2+1, w+1)
                        foundtwin+=t
    if(foundtwin>0):
        return(foundtwin)
    
    # Look for twisted triplets
    for x in range(0,3):
        for y in range(0,3):
            for za in range(0,7):
                for zb in range(za+1,8):
                    for zc in range(zb+1,9):
                        mta=m[x*3:x*3+3, y*3:y*3+3, za]
                        tmta=mta.reshape(1,9)[0]
                        mtb=m[x*3:x*3+3, y*3:y*3+3, zb]
                        tmtb=mtb.reshape(1,9)[0]
                        mtc=m[x*3:x*3+3, y*3:y*3+3, zc]
                        tmtc=mtc.reshape(1,9)[0]
                        sum3=sum(tmta+tmtb+tmtc==3)  # All 3 values eliminated
                        sum2=sum(tmta+tmtb+tmtc==2)  # Only 2 values eliminated
                        sum1=sum(tmta+tmtb+tmtc==1)  # Only one value eliminated
                        sum0=sum(tmta+tmtb+tmtc==0)  # None of values eliminated
                        if (sum3==6 and sum0>0 and sum0+sum1+sum2==3):  #(sum0==2 and sum1==1 or sum0==1 and sum1==2)):
                            idx=np.where(tmta+tmtb+tmtc<3)[0]
                            t=twistedtriplet(x, y, idx[0], idx[1], idx[2], za, zb, zc)
                            if (debug==1 and t>0):
                                print "Twisted triplets: Sq %dx%d Idx [%d %d %d] = [%d %d %d]" % \
                                (x+1, y+1, idx[0]+1, idx[1]+1, idx[2]+1, za+1, zb+1, zc+1)
                            foundtwin+=t
    if(foundtwin>0):
        return(foundtwin)
        
    # Look for quadruplets
    for x in range(0,3):
        for y in range(0,3):
            for za in range(0,6):
                for zb in range(za+1,7):
                    for zc in range(zb+1,8):
                        for zd in range(zc+1,9):
                            mta=m[x*3:x*3+3, y*3:y*3+3, za]
                            tmta=mta.reshape(1,9)[0]
                            mtb=m[x*3:x*3+3, y*3:y*3+3, zb]
                            tmtb=mtb.reshape(1,9)[0]
                            mtc=m[x*3:x*3+3, y*3:y*3+3, zc]
                            tmtc=mtc.reshape(1,9)[0]
                            mtd=m[x*3:x*3+3, y*3:y*3+3, zd]
                            tmtd=mtd.reshape(1,9)[0]                            
                            sum4=sum(tmta+tmtb+tmtc+tmtd==4)
                            sum3=sum(tmta+tmtb+tmtc+tmtd==3)
                            sum2=sum(tmta+tmtb+tmtc+tmtd==2)
                            sum1=sum(tmta+tmtb+tmtc+tmtd==1)
                            sum0=sum(tmta+tmtb+tmtc+tmtd==0)
                            #if (sum4==5 and sum0>0 and sum1>0 and sum2>0 and sum0+sum1+sum2==4):
                            if (sum4==5 and sum0>0 and sum0+sum1+sum2+sum3==4):
                                idx=np.where(tmta+tmtb+tmtc+tmtd<4)[0]
                                #print("Possible quadruplet", 
                                #      x+1, y+1, 
                                #      idx[0]+1, idx[1]+1, idx[2]+1, idx[3]+1,
                                #      za+1, zb+1, zc+1, zd+1)
                                t=quadruplet(x, y, idx[0], idx[1], idx[2], idx[3],
                                             za, zb, zc, zd)
                                if (debug==1 and t>0):
                                    print("Quadruplets",
                                      x+1, y+1, 
                                      idx[0]+1, idx[1]+1, idx[2]+1, idx[3]+1,
                                      za+1, zb+1, zc+1, zd+1)
                                foundtwin+=t
    if(foundtwin>0):
        return(foundtwin)

    # Look for quintuplets
    for x in range(0,3):
        for y in range(0,3):
            for za in range(0,5):
                for zb in range(za+1,6):
                    for zc in range(zb+1,7):
                        for zd in range(zc+1,8):
                            for ze in range(zd+1,9):
                                mta=m[x*3:x*3+3, y*3:y*3+3, za].reshape(1,9)[0]
                                mtb=m[x*3:x*3+3, y*3:y*3+3, zb].reshape(1,9)[0]
                                mtc=m[x*3:x*3+3, y*3:y*3+3, zc].reshape(1,9)[0]
                                mtd=m[x*3:x*3+3, y*3:y*3+3, zd].reshape(1,9)[0]
                                mte=m[x*3:x*3+3, y*3:y*3+3, ze].reshape(1,9)[0]
                                sum5=sum(mta+mtb+mtc+mtd+mte==5)
                                sum4=sum(mta+mtb+mtc+mtd+mte==4)
                                sum3=sum(mta+mtb+mtc+mtd+mte==3)
                                sum2=sum(mta+mtb+mtc+mtd+mte==2)
                                sum1=sum(mta+mtb+mtc+mtd+mte==1)
                                sum0=sum(mta+mtb+mtc+mtd+mte==0)
                                if (sum5==4 and sum0>0 and sum0+sum1+sum2+sum3+sum4==5):
                                    idx=np.where(mta+mtb+mtc+mtd+mte<5)[0]
                                    print("Possible quintuplet", 
                                          x+1, y+1, 
                                          idx[0]+1, idx[1]+1, idx[2]+1, idx[3]+1, idx[4]+1,
                                          za+1, zb+1, zc+1, zd+1, ze+1)
                                    #t=quintuplet(x, y, idx[0], idx[1], idx[2], idx[3], idx[4],
                                    #             za, zb, zc, zd, ze)
                                    #if (debug==1 and t>0):
                                    #    print("Quintuplets",
                                    #          x+1, y+1, 
                                    #          idx[0]+1, idx[1]+1, idx[2]+1, idx[3]+1, idx[4]+1,
                                    #          za+1, zb+1, zc+1, zd+1, ze+1)
                                    #foundtwin+=t
    if(foundtwin>0):
        return(foundtwin)



def solver(s,d=1):
    for j in range(0,len(s)):
        v=int(s[j])
        if (v>=1 and v<=9):
            #print(j/9, j%9, v)
            fill(j/9, j%9, v)
    if (d==1):
        print("Starting")
        display()                

    # Scan for cells to fill
    result=1
    while(result):
        result=scan(debug=d)

    # Check result
    sudoku=""
    for i in (range(0,9)):
        for j in (range(0,9)):
            sudoku=sudoku+str(sol[i][j])
    if (sudoku.find("0")>=0):
        print("INCOMPLETE!")
        # Dump known values
        for i in (range(0,9)):
            for j in (range(0,9)):
                if sum(m[i][j]) < 9:
                    print "%dx%d = %s" % (i+1, j+1, np.where(m[i][j]==0)[0]+1)
        return(0)
    print("SUCCESS!")    
    return(1)




# Main routine


top95=1

if (SolveThis != ""):
    solver(SolveThis, 1)
    #sys.exit(0)

elif(top95==1):
    success=0
    with open('sudoku-hard.txt') as csvfile:
        readCSV=csv.reader(csvfile, delimiter=",")
        for row in readCSV:
            puzzle=row[0]

            # Create empty data set
            
            m=np.zeros((9,9,9), dtype=int)
            sol=np.zeros((9,9), dtype=int)     
            success+=solver(puzzle, 0)
            display()
    print("Completed successfully",success)

else:
    NumMatch=0
    NumLines=0
    StartTime=time.time()
    with open('sudoku.csv') as csvfile:
        readCSV=csv.reader(csvfile, delimiter=",")
        next(readCSV, None)   # skip the header
        for row in readCSV:
            NumLines+=1
            #if (NumLines<=750000 or NumLines>1000000):
            #    continue
            puzzle=row[0]
            answer=row[1]
            # Create empty data set
            
            m=np.zeros((9,9,9), dtype=int)
            sol=np.zeros((9,9), dtype=int)     
            solver(puzzle, 0)
            
            # Check result
            sudoku=""
            for i in (range(0,9)):
                for j in (range(0,9)):
                    sudoku=sudoku+str(sol[i][j])
            if (sudoku == answer):
                NumMatch+=1
            else:
                print("FAIL!!!  At",NumLines)
                print(puzzle)
                            
    EndTime=time.time()
    print("Final results:",NumMatch,"correct out of",NumLines,"in",EndTime-StartTime,"seconds")

