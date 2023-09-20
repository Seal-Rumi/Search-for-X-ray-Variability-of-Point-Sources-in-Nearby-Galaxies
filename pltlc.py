import os
import matplotlib.pylab as plt
from astropy.io import fits

#Input bin time/bin time unit
bin_time = input("Enter bin time: ")

while True:
    bin_time_unit = input("Choose bin time unit(h/m/s): ")
    if bin_time_unit  in ["h", "m", "s"]:
        break
    else: 
        print("Please input (h/m/s).")
        continue

srclist = []
files = os.listdir(os.getcwd()+"/bary")
for filename in files:
    num = filename.split('_')[0].split("src")[-1]
    srclist.append(int(num))
srclist.sort()

#Main
directory=os.getcwd()
for i in srclist:
    lcf = "src{}_lightcurve_{}{}.fits".format(i, bin_time, bin_time_unit)
    name = lcf.split('.')[0]
    hdu = fits.open(directory+"/lcf/"+lcf, sep='')
    Time = hdu[1].data.field(2)
    Time = Time - Time[0]
    Time_Min = hdu[1].data.field(1)
    Time_Max = hdu[1].data.field(3)
    Net_Rate = hdu[1].data.field(19)
    Err_Rate = hdu[1].data.field(20)
    
    plt.figure(dpi=150)
    plt.errorbar(Time, Net_Rate, yerr=Err_Rate, \
                 marker="o", color="red", mfc="black", ecolor="gray")
    plt.title(lcf)
    plt.xlabel("$\Delta$ T (sec)")
    plt.ylabel("Net Count Rate (counts/sec)")
    plt.savefig("{}/lcimg/{}.png".format(directory,name))
    print("Output: {}.png".format(name))
    plt.close()
