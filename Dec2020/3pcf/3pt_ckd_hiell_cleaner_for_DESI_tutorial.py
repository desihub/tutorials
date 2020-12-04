#Code for DESI Virtual Meeting Tutorial: December 4, 2020.
##########################################load needed modules for python#######################################################################
#doing basic math
import numpy as np
import scipy as sp
#for sine integral
from scipy.special import *
#parsing arguments that are given in command line
import argparse
#plotting
import matplotlib.pyplot as plt
plt.matplotlib.use('PDF')
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
#interpolating
from scipy.interpolate import interp1d
#for getting latex characters in plot titles
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rcParams['ps.useafm'] = True
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rcParams['pdf.fonttype'] = 42
#plotting a density plot (2-d)
from numpy import exp,arange
from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show
#interpolation to set up functions for 2d plots
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
#for special functions: spherical bessel functions and Legendre polynomials
import scipy.special as sp
#to save multipage pdfs
from matplotlib.backends.backend_pdf import PdfPages
#for random numbers
import random as rm
#for timing
import time
#kd tree
from scipy import spatial
#######################################################setup definitions#######################################################################
#This controls if you want to read in data points from a file. I've provided a sample file, and we will try this during the tutorial.
read_from_file=1.
if read_from_file:
    boxsize = 400. #size of box used in sample data file.
    rescale = 1. #if you want to rescale the box (unity if not).
    boxsize *= rescale #this is important so the periodic duplicates are made correctly.
    galx, galy, galz, weights = np.loadtxt('sample_feb27_unity_weights_rescale400_first500.dat',unpack=True) #Put your local file title here.
    galx, galy, galz = galx*rescale, galy*rescale, galz*rescale
    print("read galaxies from file and converted using boxsize")
    print("number in file=",len(galx))

#exit()


numell=11
#throw randoms for galaxies in box.
#One needs to choose number of galaxies. I found 10,000 was the limit for a 2015 Macbook Air, likely one can do a bit more on a more modern machine.
start_time=time.clock()
linspace=0.

eightpi_sq=8.*np.pi**2
eps=1e-8
if read_from_file:
    ngal=len(galx)
else:
    ngal=50
#checked this program with counting for ngal=500, seed=35 and seed=1.
rmax=np.sqrt(3.)*5.
rmin=1e-5
nbins=3
deltr = float(rmax-rmin)/nbins
binarr=np.mgrid[0:nbins+1]*deltr
zeta0=np.zeros((nbins,nbins))+0j
zeta1=np.zeros((nbins,nbins))+0j
zeta2=np.zeros((nbins,nbins))+0j
zeta3=np.zeros((nbins,nbins))+0j
zeta4=np.zeros((nbins,nbins))+0j
zeta5=np.zeros((nbins,nbins))+0j
zeta6=np.zeros((nbins,nbins))+0j
zeta7=np.zeros((nbins,nbins))+0j
zeta8=np.zeros((nbins,nbins))+0j
zeta9=np.zeros((nbins,nbins))+0j
zeta10=np.zeros((nbins,nbins))+0j

histtime=0
bintime=0
transftime=0
end_time=time.clock()


def shiftbox(galx,galy,galz,shiftbox,doxshift,doyshift,dozshift):
    galxsh=galx+doxshift*boxsize
    galysh=galy+doyshift*boxsize
    galzsh=galz+dozshift*boxsize

    galcoordssh=list(zip(galxsh.ravel(),galysh.ravel(),galzsh.ravel()))

    return galcoordssh


print("time to set constants and bins=",end_time-start_time)

start_time=time.clock()

'''
#Save galaxy coordinates to a file for cross-checking later if you'd like.
file = open("gal_coords_3pcf_test.txt", "w")
count=0
for index in range(0,ngal,1):
    print >>file, '%5.5f %5.5f %5.5f %5.5f' % (galx[index],galy[index],galz[index], 1.0)#add a fourth column with weights to compare with 3PCF C++ code, which looks to take in weights.
file.close()
print "coordinates written to file"
'''
    
galcoords=list(zip(galx.ravel(),galy.ravel(),galz.ravel()))
#now loop over shiftbox to append virtual boxes to coordinate list.
for doxshift in (-1,1,0):
    for doyshift in (-1,1,0):
        for dozshift in (-1,1,0):
            print(doxshift,doyshift,dozshift)
            if doxshift==0 and doyshift==0 and dozshift==0:
                print("no shift executed because in genuine box")
            else:
                galcoords=np.append(galcoords,shiftbox(galx,galy,galz,boxsize,doxshift,doyshift,dozshift),axis=0) #Note axis=0 is quite important to maintain ordered triplet structure of data; if you don't include you get 27*ngals*3 values, rather than 27*ngals ordered triplets.


end_time=time.clock()

print("time to throw",ngal,"random galaxies, shift them, and zip them together= (*)",end_time-start_time)

start_time=time.clock()
#put galaxies in a tree
tree=spatial.cKDTree(galcoords,leafsize=3000)
end_time=time.clock()
print("time to put",ngal,"random galaxies in tree=(*)",end_time-start_time)

#Choose to work on first nperit galaxies.
start_time=time.clock()
nperit=ngal/1 #1 for just looking at one galaxy to see more granular timings. ngal/100 gives 20000/10=2000 per iteration.
totalits=ngal/nperit #5#ngal/nperit#5 for testing leaf size if I want to iterate over 1000 galaxies.
count=0
querytime=0.
complextime=0.
realtime=0.
for i in range(0,totalits): #do nperit galaxies at a time for totalits total iterations
    print("group number=",i)
    centralgals=galcoords[i*nperit:(i+1)*nperit] #select out central galaxies to use; note central galaxies must be first in list of coordinates including shift, which they will be by construction.
    print("len centralgals=", len(centralgals))
    print("using galaxies from", i*nperit, "to", (i+1)*nperit-1)
    print("i*nperit=",i*nperit)
    start_time_query=time.clock()
    ball=tree.query_ball_point(centralgals,rmax+eps) #object with, for each index, an array with the ball of rmax about the central galaxy of that index; e.g. ball[0] gives indices of gals. within rmax of the 0th centralgal
    end_time_query=time.clock()
    querytime=end_time_query-start_time_query+querytime
    for w in range(0,nperit):
        start_time_transf=time.clock()
        #print "bal[w]l=",ball[w]
        #print "count=",count
        #print "i*nperit+w=",i*nperit+w
        ball[w].remove(i*nperit+w)
        #print "ball[w]=",ball[w]
        #print "galaxy number within its group=",w
        #transform to reference frame of desired central galaxy
        #could I vectorize this so it's doing all 3 at the same time? no reason it needs to wait on x before doing y!  reduce time by ~1/3!
        ball_temp=ball[w]
        galxtr, galytr, galztr=galcoords[ball_temp][:,0]-centralgals[w][0],galcoords[ball_temp][:,1]-centralgals[w][1],galcoords[ball_temp][:,2]-centralgals[w][2]
        #galytr=galcoords[ball[w]][:,1]-centralgals[w][1]
        #galztr=galcoords[ball[w]][:,2]-centralgals[w][2]
        #print ball[w]
        #print galztr
        rgalssq=galxtr*galxtr+galytr*galytr+galztr*galztr+eps
        rgals=np.sqrt(rgalssq)
        #xmiydivr,xdivr,ydivr,zdivr=(galxtr-1j*galytr)/rgals,galxtr/rgals,galytr/rgals,galztr/rgals #compute (x-iy)/r for galaxies in ball around central
                                                                                                                                             #zdivr=galztr/rgals
                                                                                                                                             #xdivr=galxtr/rgals
                                                                                                                                             #ydivr=galytr/rgals
        xmiydivr,xdivr,ydivr,zdivr=(galxtr-1j*galytr),galxtr,galytr,galztr#broke this to see how not dividing by r affects results. #compute (x-iy)/r for galaxies in ball around central


        #compute squares: need to replace inline computations using these below.
        xdivrsq=xdivr*xdivr
        ydivrsq=ydivr*ydivr
        zdivrsq=zdivr*zdivr
        xmiydivrsq=xmiydivr*xmiydivr
        xmiydivrcu=xmiydivrsq*xmiydivr
        xmiydivrft=xmiydivrcu*xmiydivr
        xmiydivrfi=xmiydivrft*xmiydivr
        xmiydivrsi=xmiydivrfi*xmiydivr
        xmiydivrse=xmiydivrsi*xmiydivr
        xmiydivret=xmiydivrse*xmiydivr
        xmiydivrni=xmiydivret*xmiydivr
        xmiydivrtn=xmiydivrni*xmiydivr

        zdivrcu=zdivrsq*zdivr
        zdivrft=zdivrsq*zdivrsq
        zdivrfi=zdivrft*zdivr
        zdivrsi=zdivrfi*zdivr
        zdivrse=zdivrsi*zdivr
        zdivret=zdivrse*zdivr
        zdivrni=zdivret*zdivr
        zdivrtn=zdivrni*zdivr
        #compute spherical harmonics on all bins for this galaxy; query_ball finds central itself too but this doesn't contribute to spherical harmonics because x, y, z are zero.
        #newly added sept 2.
        end_time_transf=time.clock()
        transftime=end_time_transf-start_time_transf+transftime
        start_time_hist=time.clock()
        y00=.5*(1./np.pi)**.5*np.histogram(rgals,bins=binarr)[0]
        complex_test_start=time.clock()
        y1m1=.5*(3./(2.*np.pi))**.5*np.histogram(rgals,bins=binarr,weights=xmiydivr)[0] #this just gives histogram y values; [1] would give bin edges with length of [0] + 1.
        complex_test_end=time.clock()
        complextime=complex_test_end-complex_test_start+complextime
        real_test_start=time.clock()
        y1m1test=.5*(3./(2.*np.pi))**.5*(np.histogram(rgals,bins=binarr,weights=xdivr)[0]-1j*np.histogram(rgals,bins=binarr,weights=ydivr)[0])
        real_test_end=time.clock()
        realtime=real_test_end-real_test_start+realtime
        y10=.5*(3./np.pi)**.5*np.histogram(rgals,bins=binarr,weights=zdivr)[0]
        y2m2=.25*(15./(2.*np.pi))**.5*np.histogram(rgals,bins=binarr,weights=xmiydivrsq)[0]
        y2m1=.5*(15./(2.*np.pi))**.5*np.histogram(rgals,bins=binarr,weights=xmiydivr*zdivr)[0]
        y20=.25*(5./np.pi)**.5*np.histogram(rgals,bins=binarr,weights=2.*zdivrsq-xdivrsq-ydivrsq)[0]
        y3m3=.125*(35./np.pi)**.5*np.histogram(rgals,bins=binarr,weights=xmiydivrcu)[0]
        y3m2=.25*(105./(2.*np.pi))**.5*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*zdivr)[0]
        y3m1=.125*(21./np.pi)**.5*np.histogram(rgals,bins=binarr,weights=xmiydivr*(4.*zdivrsq-xdivrsq-ydivrsq))[0]
        y30=.25*(7./np.pi)**.5*np.histogram(rgals,bins=binarr,weights=zdivr*(2.*zdivrsq-3.*xdivrsq-3.*ydivrsq))[0]
        #newly added sept 2.
        y4m4=.1875*np.sqrt(35./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft)[0]
        y4m3=.375*np.sqrt(35./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*zdivr)[0]
        y4m2=.375*np.sqrt(5./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(7.*zdivrsq-1))[0]
        y4m1=.375*np.sqrt(5./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivr*zdivr*(7.*zdivrsq-3.))[0]
        y40=.1875*np.sqrt(1./np.pi)*np.histogram(rgals,bins=binarr,weights=(35.*zdivrft-30.*zdivrsq+3.))[0]
        
        y5m5=(3./32.)*np.sqrt(77./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrfi)[0]
        y5m4=(3./16.)*np.sqrt(385./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft*zdivr)[0]
        y5m3=(1./32.)*np.sqrt(385./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*(9.*zdivrsq-1.))[0]
        y5m2=(1./8.)*np.sqrt(1155./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(3.*zdivrcu-zdivr))[0]
        y5m1=(1./16.)*np.sqrt(165./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivr*(21.*zdivrft-14.*zdivrsq+1.))[0]
        y50=(1./16.)*np.sqrt(11./np.pi)*np.histogram(rgals,bins=binarr,weights=63.*zdivrfi-70.*zdivrcu+15.*zdivr)[0]

        y6m6=(1./64.)*np.sqrt(3003./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsi)[0]
        y6m5=(3./32.)*np.sqrt(1001./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrfi*zdivr)[0]
        y6m4=(3./32.)*np.sqrt(91./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft*(11.*zdivrsq-1.))[0]
        y6m3=(1./32.)*np.sqrt(1365./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*(11.*zdivrcu-3.*zdivr))[0]
        y6m2=(1./64.)*np.sqrt(1365./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(33.*zdivrft-18.*zdivrsq+1.))[0]
        y6m1=(1./16.)*np.sqrt(273./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivr*(33.*zdivrfi-30.*zdivrcu+5.*zdivr))[0]
        y60=(1./32.)*np.sqrt(13./np.pi)*np.histogram(rgals,bins=binarr,weights=231.*zdivrsi-315.*zdivrft+105.*zdivrsq-5.)[0]

        y7m7=(3./64.)*np.sqrt(715./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrse)[0]
        y7m6=(3./64.)*np.sqrt(5005./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsi*zdivr)[0]
        y7m5=(3./64.)*np.sqrt(385./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrfi*(13.*zdivrsq-1.))[0]
        y7m4=(3./32.)*np.sqrt(385./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft*(13.*zdivrcu-3.*zdivr))[0]
        y7m3=(3./64.)*np.sqrt(35./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*(143.*zdivrft-66.*zdivrsq+3.))[0]
        y7m2=(3./64.)*np.sqrt(35./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(143.*zdivrfi-110.*zdivrcu+15.*zdivr))[0]
        y7m1=(1./64.)*np.sqrt(105./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivr*(429.*zdivrsi-495.*zdivrft+135.*zdivrsq-5.))[0]
        y70=(1./32.)*np.sqrt(15./np.pi)*np.histogram(rgals,bins=binarr,weights=429.*zdivrse-693.*zdivrfi+315.*zdivrcu-35.*zdivr)[0]

        y8m8=(3./256.)*np.sqrt(12155./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivret)[0]
        y8m7=(3./64.)*np.sqrt(12155./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrse*zdivr)[0]
        y8m6=(1./128.)*np.sqrt(7293./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsi*(15.*zdivrsq-1.))[0]
        y8m5=(3./64.)*np.sqrt(17017./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrfi*(5.*zdivrcu-zdivr))[0]
        y8m4=(3./128.)*np.sqrt(1309./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft*(65.*zdivrft-26.*zdivrsq+1.))[0]
        y8m3=(1./64.)*np.sqrt(19635./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*(39.*zdivrfi-26.*zdivrcu+3.*zdivr))[0]
        y8m2=(3./128.)*np.sqrt(595./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(143.*zdivrsi-143.*zdivrft+33.*zdivrsq-1.))[0]
        y8m1=(3./64.)*np.sqrt(17./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivr*(715.*zdivrse-1001.*zdivrfi+385.*zdivrcu-35.*zdivr))[0]
        y80=(1./256.)*np.sqrt(17./np.pi)*np.histogram(rgals,bins=binarr,weights=6435.*zdivret-12012.*zdivrsi+6930.*zdivrft-1260.*zdivrsq+35.)[0]

        y9m9=(1./512.)*np.sqrt(230945./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrni)[0]
        y9m8=(3./256.)*np.sqrt(230945./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivret*zdivr)[0]
        y9m7=(3./512.)*np.sqrt(13585./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrse*(17.*zdivrsq-1.))[0]
        y9m6=(1./128.)*np.sqrt(40755./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsi*(17.*zdivrcu-3.*zdivr))[0]
        y9m5=(3./256.)*np.sqrt(2717./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrfi*(85.*zdivrft-30.*zdivrsq+1.))[0]
        y9m4=(3./128.)*np.sqrt(95095./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft*(17.*zdivrfi-10.*zdivrcu+zdivr))[0]
        y9m3=(1./256.)*np.sqrt(21945./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*(221.*zdivrsi-195.*zdivrft+39.*zdivrsq-1.))[0]
        y9m2=(3./128.)*np.sqrt(1045./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(221.*zdivrse-273.*zdivrfi+91.*zdivrcu-7.*zdivr))[0]
        y9m1=(3./256.)*np.sqrt(95./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivr*(2431.*zdivret-4004.*zdivrsi+2002.*zdivrft-308.*zdivrsq+7.))[0]
        y90=(1./256.)*np.sqrt(19./np.pi)*np.histogram(rgals,bins=binarr,weights=12155.*zdivrni-25740.*zdivrse+18018.*zdivrfi-4620.*zdivrcu+315.*zdivr)[0]

        y10m10=(1./1024.)*np.sqrt(969969./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrtn)[0]
        y10m9=(1./512.)*np.sqrt(4849845./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrni*zdivr)[0]
        y10m8=(1./512.)*np.sqrt(255255./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivret*(19.*zdivrsq-1.))[0]
        y10m7=(3./512.)*np.sqrt(85085./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrse*(19.*zdivrcu-3.*zdivr))[0]
        y10m6=(3./1024.)*np.sqrt(5005./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrsi*(323.*zdivrft-102.*zdivrsq+3.))[0]
        y10m5=(3./256.)*np.sqrt(1001./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrfi*(323.*zdivrfi-170.*zdivrcu+15.*zdivr))[0]
        y10m4=(3./256.)*np.sqrt(5005./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrft*(323.*zdivrsi-255.*zdivrft+45.*zdivrsq-1.))[0]
        y10m3=(3./256.)*np.sqrt(5005./np.pi)*np.histogram(rgals,bins=binarr,weights=xmiydivrcu*(323.*zdivrse-357.*zdivrfi+105.*zdivrcu-7.*zdivr))[0]
        y10m2=(3./512.)*np.sqrt(385./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivrsq*(4199.*zdivret-6188.*zdivrsi+2730.*zdivrft-364.*zdivrsq+7.))[0]
        y10m1=(1./256.)*np.sqrt(1155./(2.*np.pi))*np.histogram(rgals,bins=binarr,weights=xmiydivr*(4199.*zdivrni-7956.*zdivrse+4914.*zdivrfi-1092.*zdivrcu+63.*zdivr))[0]
        y100=(1./512.)*np.sqrt(21./np.pi)*np.histogram(rgals,bins=binarr,weights=46189.*zdivrtn-109395.*zdivret+90090.*zdivrsi-30030.*zdivrft+3465.*zdivrsq-63.)[0]
        
        
        end_time_hist=time.clock()
        histtime=end_time_hist-start_time_hist+histtime
        count=count+1
        start_time_binning=time.clock()
        bin_val = np.zeros(nbins*nbins)
        ii = 0
        for bin1 in range(nbins):
            for bin2 in range(nbins):#this computes only upper diagonal of matrix and avoids doing diagonal---so no double counting.
            #for bin2 in range(bin1+1):#this computes only upper diagonal of matrix and avoids doing diagonal---so no double counting.
                #print "bin1, bin2=", bin1, bin2
                bin_val[ii] = (bin1+.5)*(bin2+.5)  
                zeta0[bin1,bin2]=y00[bin1]*y00[bin2].conjugate()+zeta0[bin1,bin2]#do we need this second term?
                zeta1[bin1,bin2]=(y1m1[bin1]*y1m1[bin2].conjugate()+y10[bin1]*y10[bin2].conjugate()+y1m1[bin1].conjugate()*y1m1[bin2])+zeta1[bin1,bin2]
                zeta2[bin1,bin2]=(y2m2[bin1]*y2m2[bin2].conjugate()+y2m1[bin1]*y2m1[bin2].conjugate()+y20[bin1]*y20[bin2].conjugate()+y2m1[bin1].conjugate()*y2m1[bin2]+y2m2[bin1].conjugate()*y2m2[bin2])+zeta2[bin1,bin2]
                zeta3[bin1,bin2]=(y3m3[bin1]*y3m3[bin2].conjugate()+y3m2[bin1]*y3m2[bin2].conjugate()+y3m1[bin1]*y3m1[bin2].conjugate()+y30[bin1]*y30[bin2].conjugate()+y3m1[bin1].conjugate()*y3m1[bin2]+y3m2[bin1].conjugate()*y3m2[bin2]+y3m3[bin1].conjugate()*y3m3[bin2])+zeta3[bin1,bin2]
                zeta4[bin1,bin2]=(y4m4[bin1]*y4m4[bin2].conjugate()+y4m3[bin1]*y4m3[bin2].conjugate()+y4m2[bin1]*y4m2[bin2].conjugate()+y4m1[bin1]*y4m1[bin2].conjugate()+y40[bin1]*y40[bin2].conjugate()+y4m1[bin1].conjugate()*y4m1[bin2]+y4m2[bin1].conjugate()*y4m2[bin2]+y4m3[bin1].conjugate()*y4m3[bin2]+y4m4[bin1].conjugate()*y4m4[bin2])+zeta4[bin1,bin2]

                zeta5[bin1,bin2]=(y5m5[bin1]*y5m5[bin2].conjugate()+y5m4[bin1]*y5m4[bin2].conjugate()+y5m3[bin1]*y5m3[bin2].conjugate()+y5m2[bin1]*y5m2[bin2].conjugate()+y5m1[bin1]*y5m1[bin2].conjugate()+y50[bin1]*y50[bin2].conjugate()+y5m1[bin1].conjugate()*y5m1[bin2]+y5m2[bin1].conjugate()*y5m2[bin2]+y5m3[bin1].conjugate()*y5m3[bin2]+y5m4[bin1].conjugate()*y5m4[bin2]+y5m5[bin1].conjugate()*y5m5[bin2])+zeta5[bin1,bin2]
                zeta6[bin1,bin2]=(y6m6[bin1]*y6m6[bin2].conjugate()+y6m5[bin1]*y6m5[bin2].conjugate()+y6m4[bin1]*y6m4[bin2].conjugate()+y6m3[bin1]*y6m3[bin2].conjugate()+y6m2[bin1]*y6m2[bin2].conjugate()+y6m1[bin1]*y6m1[bin2].conjugate()+y60[bin1]*y60[bin2].conjugate()+y6m1[bin1].conjugate()*y6m1[bin2]+y6m2[bin1].conjugate()*y6m2[bin2]+y6m3[bin1].conjugate()*y6m3[bin2]+y6m4[bin1].conjugate()*y6m4[bin2]+y6m5[bin1].conjugate()*y6m5[bin2]+y6m6[bin1].conjugate()*y6m6[bin2])+zeta6[bin1,bin2]
                zeta7[bin1,bin2]=(y7m7[bin1]*y7m7[bin2].conjugate()+y7m6[bin1]*y7m6[bin2].conjugate()+y7m5[bin1]*y7m5[bin2].conjugate()+y7m4[bin1]*y7m4[bin2].conjugate()+y7m3[bin1]*y7m3[bin2].conjugate()+y7m2[bin1]*y7m2[bin2].conjugate()+y7m1[bin1]*y7m1[bin2].conjugate()+y70[bin1]*y70[bin2].conjugate()+y7m1[bin1].conjugate()*y7m1[bin2]+y7m2[bin1].conjugate()*y7m2[bin2]+y7m3[bin1].conjugate()*y7m3[bin2]+y7m4[bin1].conjugate()*y7m4[bin2]+y7m5[bin1].conjugate()*y7m5[bin2]+y7m6[bin1].conjugate()*y7m6[bin2]+y7m7[bin1].conjugate()*y7m7[bin2])+zeta7[bin1,bin2]
                zeta8[bin1,bin2]=(y8m8[bin1]*y8m8[bin2].conjugate()+y8m7[bin1]*y8m7[bin2].conjugate()+y8m6[bin1]*y8m6[bin2].conjugate()+y8m5[bin1]*y8m5[bin2].conjugate()+y8m4[bin1]*y8m4[bin2].conjugate()+y8m3[bin1]*y8m3[bin2].conjugate()+y8m2[bin1]*y8m2[bin2].conjugate()+y8m1[bin1]*y8m1[bin2].conjugate()+y80[bin1]*y80[bin2].conjugate()+y8m1[bin1].conjugate()*y8m1[bin2]+y8m2[bin1].conjugate()*y8m2[bin2]+y8m3[bin1].conjugate()*y8m3[bin2]+y8m4[bin1].conjugate()*y8m4[bin2]+y8m5[bin1].conjugate()*y8m5[bin2]+y8m6[bin1].conjugate()*y8m6[bin2]+y8m7[bin1].conjugate()*y8m7[bin2]+y8m8[bin1].conjugate()*y8m8[bin2])+zeta8[bin1,bin2]
                zeta9[bin1,bin2]=(y9m9[bin1]*y9m9[bin2].conjugate()+y9m8[bin1]*y9m8[bin2].conjugate()+y9m7[bin1]*y9m7[bin2].conjugate()+y9m6[bin1]*y9m6[bin2].conjugate()+y9m5[bin1]*y9m5[bin2].conjugate()+y9m4[bin1]*y9m4[bin2].conjugate()+y9m3[bin1]*y9m3[bin2].conjugate()+y9m2[bin1]*y9m2[bin2].conjugate()+y9m1[bin1]*y9m1[bin2].conjugate()+y90[bin1]*y90[bin2].conjugate()+y9m1[bin1].conjugate()*y9m1[bin2]+y9m2[bin1].conjugate()*y9m2[bin2]+y9m3[bin1].conjugate()*y9m3[bin2]+y9m4[bin1].conjugate()*y9m4[bin2]+y9m5[bin1].conjugate()*y9m5[bin2]+y9m6[bin1].conjugate()*y9m6[bin2]+y9m7[bin1].conjugate()*y9m7[bin2]+y9m8[bin1].conjugate()*y9m8[bin2]+y9m9[bin1].conjugate()*y9m9[bin2])+zeta9[bin1,bin2]
                zeta10[bin1,bin2]=(y10m10[bin1]*y10m10[bin2].conjugate()+y10m9[bin1]*y10m9[bin2].conjugate()+y10m8[bin1]*y10m8[bin2].conjugate()+y10m7[bin1]*y10m7[bin2].conjugate()+y10m6[bin1]*y10m6[bin2].conjugate()+y10m5[bin1]*y10m5[bin2].conjugate()+y10m4[bin1]*y10m4[bin2].conjugate()+y10m3[bin1]*y10m3[bin2].conjugate()+y10m2[bin1]*y10m2[bin2].conjugate()+y10m1[bin1]*y10m1[bin2].conjugate()+y100[bin1]*y100[bin2].conjugate()+y10m1[bin1].conjugate()*y10m1[bin2]+y10m2[bin1].conjugate()*y10m2[bin2]+y10m3[bin1].conjugate()*y10m3[bin2]+y10m4[bin1].conjugate()*y10m4[bin2]+y10m5[bin1].conjugate()*y10m5[bin2]+y10m6[bin1].conjugate()*y10m6[bin2]+y10m7[bin1].conjugate()*y10m7[bin2]+y10m8[bin1].conjugate()*y10m8[bin2]+y10m9[bin1].conjugate()*y10m9[bin2]+y10m10[bin1].conjugate()*y10m10[bin2])+zeta10[bin1,bin2]
                ii += 1
                

        end_time_binning=time.clock()
        bintime=end_time_binning-start_time_binning+bintime

        #if i==0:
            #if w==2:
            #print "centralgals=",centralgals[w][0],centralgals[w][1],centralgals[w][2]
            #  zeta1save=zeta1*addthmfac[1]/2.
            #  zeta2save=zeta2*addthmfac[2]/2.
            #   zeta3save=zeta3*addthmfac[3]/2.
            #   print zeta1save
            #   print zeta2save
            #  print zeta3save


zeta0 *= 1./(4.*np.pi)#2.*np.pi this latter factor was to agree with Eisenstein C++ code, which we now know also does not have right normalization factor, but that cancels out in edge correction.
zeta1 *= 1./(4.*np.pi)
zeta2 *= 1./(4.*np.pi)
zeta3 *= 1./(4.*np.pi)
zeta4 *= 1./(4.*np.pi)
zeta5 *= 1./(4.*np.pi)
zeta6 *= 1./(4.*np.pi)
zeta7 *= 1./(4.*np.pi)
zeta8 *= 1./(4.*np.pi)
zeta9 *= 1./(4.*np.pi)
zeta10 *= 1./(4.*np.pi)

print("number of galaxies done=", count)

print("zeta0=",zeta0)
print("zeta1=",zeta1)
print("zeta2=",zeta2)
print("zeta3=",zeta3)
print("zeta4=",zeta4)
postfix = 'DESI_Tutorial_results' #Use this to tile arrays you save.
np.save('zeta0test_'+postfix,zeta0)
np.save('zeta1test_'+postfix,zeta1)
np.save('zeta2test_'+postfix,zeta2)
np.save('zeta3test_'+postfix,zeta3)
np.save('zeta4test_'+postfix,zeta4)
np.save('zeta5test_'+postfix,zeta5)
np.save('zeta6test_'+postfix,zeta6)
np.save('zeta7test_'+postfix,zeta7)
np.save('zeta8test_'+postfix,zeta8)
np.save('zeta9test_'+postfix,zeta9)
np.save('zeta10test_'+postfix,zeta10)
print("results saved to 10 numpy array files")

print("--------------------")
print("--------------------")
print("--------------------")

#print to match Eisenstein C++ code output format
for bin1 in np.arange(0,nbins):
    for bin2 in np.arange(0,nbins/2+1)[::-1]:
        if bin2<=bin1:
            print("#B1 B2 l=0 l=1            l=2          l=3                    l=4")
            print(bin1, bin2, np.real(zeta0[bin1,bin2]),np.real(zeta1[bin1,bin2]),np.real(zeta2[bin1,bin2]),np.real(zeta3[bin1,bin2]),np.real(zeta4[bin1,bin2]),np.real(zeta5[bin1,bin2]),np.real(zeta6[bin1,bin2]),np.real(zeta7[bin1,bin2]),np.real(zeta8[bin1,bin2]),np.real(zeta9[bin1,bin2]))
            #print bin1, bin2, np.real(zeta0[bin1,bin2])*2,np.real(zeta1[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta2[bin1,bin2])/ np.real(zeta0[bin1,bin2]),np.real(zeta3[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta4[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta5[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta6[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta7[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta8[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta9[bin1,bin2])/np.real(zeta0[bin1,bin2]),np.real(zeta10[bin1,bin2])/np.real(zeta0[bin1,bin2])


end_time=time.clock()
timecost=end_time-start_time
ballfrac=querytime/timecost
print("ngal=", ngal, "time for computation=",timecost)
print("fraction of time for query_ball=",ballfrac)
print("histtime=", histtime)
print("bintime=",bintime)
print("transformation time", transftime)
print("ball query time=", querytime)
print("transftime+bintime+histtime+balltime=",transftime+histtime+bintime+querytime)
print("complextesttime=",complextime)
print("realtesttime=",realtime)



#----
#Load back in results, if you like.
postfix = 'DESI_Tutorial_results.npy'
z0 = np.load('zeta0test_'+postfix)
z1 = np.load('zeta1test_'+postfix)
z2 = np.load('zeta2test_'+postfix)
z3 = np.load('zeta3test_'+postfix)
z4 = np.load('zeta4test_'+postfix)
z5 = np.load('zeta5test_'+postfix)
z6 = np.load('zeta6test_'+postfix)
z7 = np.load('zeta7test_'+postfix)
z8 = np.load('zeta8test_'+postfix)
z9 = np.load('zeta9test_'+postfix)
z10 = np.load('zeta10test_'+postfix)




exit()

###########direct counting to compare
docheck=0.
if docheck:
    start_time=time.clock()
    zeta0ct=np.zeros((nbins,nbins))+0j
    zeta1ct=np.zeros((nbins,nbins))+0j
    zeta2ct=np.zeros((nbins,nbins))+0j
    zeta3ct=np.zeros((nbins,nbins))+0j
    zeta4ct=np.zeros((nbins,nbins))+0j
    zeta5ct=np.zeros((nbins,nbins))+0j
    zeta6ct=np.zeros((nbins,nbins))+0j
    zeta7ct=np.zeros((nbins,nbins))+0j
    zeta8ct=np.zeros((nbins,nbins))+0j
    zeta9ct=np.zeros((nbins,nbins))+0j
    zeta10ct=np.zeros((nbins,nbins))+0j

    count2=0
    for m in range(0,ngal):
        print("m=", m)
        centralgal=galcoords[m]
        ballct=tree.query_ball_point(centralgal,rmax+eps)
        #print "ballct=",ballct
        lenballct=len(ballct)
        #print "ballct.remove(m)"
        ballct.remove(m) # this step is absolutely essential or counting method will be incorrect! this removes the self term.
        galxtrct=galcoords[ballct][:,0]-centralgal[0]
        galytrct=galcoords[ballct][:,1]-centralgal[1]
        galztrct=galcoords[ballct][:,2]-centralgal[2]
        print("ballct=", ballct)
        print("galcoords", galcoords)
        #exit()
        
        #galxtrct=galx[ballct]-centralgal[0]
        #galytrct=galy[ballct]-centralgal[1]
        #galztrct=galz[ballct]-centralgal[2]
        galrtrct=(galxtrct**2+galytrct**2+galztrct**2+eps)**.5
        print("galrtrct=", galrtrct)
        for k in range(lenballct-1):
            #print "m, k", m, ballct[k]
            for h in range(lenballct-1):
                #calculate relative angle using a dot product: note that central galaxy gets included but contributes nothing.
                costheta=(galxtrct[k]*galxtrct[h]+galytrct[k]*galytrct[h]+galztrct[k]*galztrct[h])/(galrtrct[k]*galrtrct[h])           
                #print "costheta=",costheta
                p0=1.
                p1=costheta
                p2=.5*(3.*costheta**2-1.)
                p3=.5*(5.*costheta**3-3.*costheta)
                p4=.125*(35.*costheta**4-30.*costheta**2+3.)
                p5=.125*(63.*costheta**5-70.*costheta**3+15.*costheta)
                p6=.0625*(231.*costheta**6-315.*costheta**4+105.*costheta**2-5.)
                p7=.0625*(-35.*costheta + 315.*costheta**3 - 693.*costheta**5 + 429.*costheta**7)
                p8=(1./128.)*(35.-1260.*costheta**2+6930.*costheta**4-12012.*costheta**6+6435.*costheta**8)
                p9=(1./128.)*(315.*costheta-4620.*costheta**3+18018.*costheta**5-25740.*costheta**7+12155.*costheta**9)
                p10=(1./256.)*(-63.+3465*costheta**2-30030.*costheta**4+90090.*costheta**6-109395.*costheta**8+46189.*costheta**10)
                #print "p1,p2,p3=",p1,p2,p3
                bin1=int(galrtrct[k]/deltr)
                bin2=int(galrtrct[h]/deltr)
                #print "bin1, bin2=", bin1, bin2
                zeta0ct[bin1,bin2]=p0+zeta0ct[bin1,bin2]
                zeta1ct[bin1,bin2]=p1+zeta1ct[bin1,bin2]
                zeta2ct[bin1,bin2]=p2+zeta2ct[bin1,bin2]
                zeta3ct[bin1,bin2]=p3+zeta3ct[bin1,bin2]
                zeta4ct[bin1,bin2]=p4+zeta4ct[bin1,bin2]
                zeta5ct[bin1,bin2]+=p5
                zeta6ct[bin1,bin2]+=p6
                zeta7ct[bin1,bin2]+=p7
                zeta8ct[bin1,bin2]+=p8
                zeta9ct[bin1,bin2]+=p9
                zeta10ct[bin1,bin2]+=p10
                #print "k,h",k,h, "zeta2ct=",zeta2ct




        count2=count2+1

    #if m==2:
    #   print "galcoords ct=", galcoords[m]
    #   zeta1ctsave=zeta1ct/2.
    #   print zeta1ctsave

#p2 is not zero for costheta=0, so it is actually counting the self term, i.e. when the satellite galaxy is the central, you are done for! note this was not an issue in older (noncyclic) version because in that version, we weren't using kdtrees and hence we did not pick up the self term when we were finding neighbors.


#what is correct factor here? may 27 2015.
    zeta0ct *= (1./2.)/eightpi_sq
    zeta1ct *= (3./2.)/eightpi_sq
    zeta2ct *= (5./2.)/eightpi_sq
    zeta3ct *= (7./2.)/eightpi_sq
    zeta4ct *= (9./2.)/eightpi_sq
    zeta5ct *= (11./2.)/eightpi_sq
    zeta6ct *= (13./2.)/eightpi_sq
    zeta7ct *= (15./2.)/eightpi_sq
    zeta8ct *= (17./2.)/eightpi_sq
    zeta9ct *= (19./2.)/eightpi_sq
    zeta10ct *= (21./2.)/eightpi_sq
    end_time=time.clock()
    timecostct=end_time-start_time
    print("timecostct=", timecostct)

#check symmetry
#print "zeta1 check", sum(abs(zeta1-np.transpose(zeta1)))
#print "zeta2 check", sum(abs(zeta2-np.transpose(zeta2)))
#print "zeta3 check", sum(abs(zeta3-np.transpose(zeta3)))

#print "zeta1ct check", sum(abs(zeta1ct-np.transpose(zeta1ct)))
#print "zeta2ct check", sum(abs(zeta2ct-np.transpose(zeta2ct)))
#print "zeta3ct check", sum(abs(zeta3ct-np.transpose(zeta3ct)))

    print("zeta0 comparison check", zeta0-zeta0ct)
    print("zeta1 comparison check", zeta1-zeta1ct)
    print("zeta2 comparison check", zeta2-zeta2ct)
    print("zeta3 comparison check", zeta3-zeta3ct)
    print("zeta4 comparison check", zeta4-zeta4ct)
    print("zeta5 comparison check", zeta5-zeta5ct)
    print("zeta6 comparison check", zeta6-zeta6ct)
    print("zeta7 comparison check", zeta7-zeta7ct)
    print("zeta8 comparison check", zeta8-zeta8ct)
    print("zeta9 comparison check", zeta9-zeta9ct)
    print("zeta10 comparison check", zeta10-zeta10ct)



#can I use same structure idea to add spherical harmonics one at a time to relevant bin? i.e. avoid using histogram---but on the other hand, using histogram, if it works how stephen says, would not be a problem.
