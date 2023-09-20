import datetime
import numpy
from matplotlib import pyplot as plt
from astropy.io import fits
import os
#---建立系統環境---#
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
#---主函數(Main)---#
def z2test_cpucalculate(t,freq):
    nfreq = numpy.array(freq)
    ntime = numpy.array(t)
    ntime = ntime - ntime[0]
    PI = numpy.pi
    n = len(nfreq)
    m = len(t)
    Zarr = numpy.array([0]*n)
    
    for i in range(n):
        phi = 2*PI*nfreq[i]*ntime
        s1 = numpy.sin(phi)
        c1 = numpy.cos(phi)
        ss1 = numpy.sum(s1)
        sc1 = numpy.sum(c1)
        Zarr[i] = (2/m)*(ss1*ss1+sc1*sc1)
        
        s2 = numpy.sin(2*phi)
        c2 = numpy.cos(2*phi)
        ss2 = numpy.sum(s2)
        sc2 = numpy.sum(c2)
        Zarr[i] =(ss1*ss1+sc1*sc1+ss2*ss2+sc2*sc2)
    return Zarr.tolist()

###Main
 
srclist = []
files = os.listdir(os.getcwd()+"/bary")
for filename in files:
    num = filename.split('_')[0].split("src")[-1]
    srclist.append(int(num))
srclist.sort()

#Mode
modes = ['all', 'sp']   #all_src, specific
while True:
    mode = input("Choose a specific mode (all/sp): ")
    if mode not in modes:
        continue
    else:
        if mode == 'all':
            break
        else:
            while True:
                flag = 0
                s = input("Source(separated by spacebar): ").split(' ')
                srclist = [src for src in s]
                for i in srclist:
                    if not i.isdigit():
                        print("Please input integer!")
                        flag = 1
                        break
                if flag:continue
                else:break
        break
#Ofac
while True:
    try:
        ofac = int(input("Input ofac:"))
    except:
        print("Please input a positive integer!")
        continue
    if ofac >0:
        break 
    else:
        print("Please input a positive integer!")   
        
obsid = os.getcwd().split('/')[-2]
logf = open("{:}/ztestdata.reg".format(os.getcwd()),'a+')
for i in srclist:
	baryf = "src{}_events_bary.fits".format(i)
	name = baryf.split('.')[0]
	hdu = fits.open("bary/{:}".format(baryf))
	t=hdu[1].data.field(0).tolist()
	Energy=hdu[1].data.field(15)
	maxlength = 50000
	pmin, pmax = 3, 20
	fmin, fmax = 1/pmax, 1/pmin
	try:
		fw = 0.5/(t[-1]-t[0])
	except:
		continue
	res = fw/ofac
	num = (fmax-fmin)//res
	nn = int(num//maxlength)
	mm = int(num%maxlength)
	mp, mf = 0, 0
	
	print("\nStarting: src{:}_ztest".format(i))
	start = datetime.datetime.now()  

	freq = [fmin]
	period = [pmax]
	while freq[-1]<fmax:
		freq.append(freq[-1] + res)
		period.append(1/freq[-1])		
	'''
	for k in range(mm-1):
		freq.append(freq[-1] + res)
		period.append(1/freq[-1])
	'''    
	z2_p = z2test_cpucalculate(t,freq)
	maxz2 = max(z2_p)
	index = z2_p.index(max(z2_p))
	mp, mf = period[index], 1/period[index]
	plt.plot(period, z2_p,'black')

	#Plot
	plt.title("Ztest: {}(ofac = {:.2e})".format(name,ofac))
	plt.xlabel('period')
	plt.ylabel('z^2')
	#plt.xlim(pmin,pmax)
	plt.savefig("ztest/obsid{:}src{:}_ztest.png".format(obsid,i))
	index = z2_p.index(max(z2_p))
	plt.close()
	print("Period: {:.6f}, Freq: {:.6f}".format(period[index], 1/period[index]))
	print("Z^2: {:.3f}".format(max(z2_p)))
	logf.write("src{:}_ztest\n".format(i))
	logf.write("Period: {:.6f}, Freq: {:.6f}\n".format(period[index], 1/period[index]))
	logf.write("Z^2: {:.3f}\n\n".format(max(z2_p)))
	end = datetime.datetime.now()             
	print("Execute time:", end - start)
logf.close()
