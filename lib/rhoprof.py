import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

def fit_func(z,rho_l,rho_v,z0,d):
    return 0.5*(rho_l + rho_v) - 0.5*(rho_l - rho_v)*np.tanh((z-z0)/(d))    



temps = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1.0]

for temp in temps:
    data = np.genfromtxt("rho_prof_Temp_{}.dat".format(temp),skip_header=4)
    # gsigma = max(data[:,3])
    # max_index = np.where(data[:,3] == gsigma)
    # data[:,1] = data[:,1] - data[max_index,1]
    plt.plot(data[:,1],data[:,3],lw=2.5,label=r"$T = {}$".format(temp))

plt.xlim(-25,25)
plt.legend(loc="best",fontsize=14.5)
plt.ylim(-0.025,1.0)
plt.xlabel(r"$z (\sigma)$",fontsize=22)
plt.ylabel(r"$\rho (m/\sigma^3)$",fontsize=22)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.minorticks_on()
plt.tight_layout()
# plt.savefig("full-density-prof.pdf")
plt.show()

rholiquid = []
rhovapor = [] 
zz0 = [] 
dd = []
plt.figure()
for temp in temps:
    data = np.genfromtxt("rho_prof_Temp_{}.dat".format(temp),skip_header=4)
    # if temp >= 0.9:
    #     gsigma = max(data[:,3])
    #     max_index = np.where(data[:,3] == gsigma)
    #     data[:,1] = data[:,1] - data[max_index,1]

    newz = []
    newrhoz = []
    for i,val in enumerate(data[:,1]):
        if val >= 0:
            newz.append(val)
            newrhoz.append(data[i,3])
    newz = np.array(newz)
    newrhoz = np.array(newrhoz)
    popt,pcov = curve_fit(fit_func,newz,newrhoz,maxfev=5000)
    rholiquid.append(popt[0])
    rhovapor.append(popt[1])
    zz0.append(popt[2])
    dd.append(popt[3])

    plt.plot(newz,newrhoz,lw=2.5,label=r"$T = {}$".format(temp))
    #plt.plot(newz,fit_func(newz,*popt),label="fit",color="red")
plt.legend(loc="best",fontsize=16.5)
plt.xlim(0,25)
plt.ylim(-0.025,1.0)
plt.xlabel(r"$z (\sigma)$",fontsize=22)
plt.ylabel(r"$\rho (m/\sigma^3)$",fontsize=22)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.minorticks_on()
plt.tight_layout()
# plt.savefig("density-prof.pdf")
plt.show()

rholiquid = np.array(rholiquid)
rhovapor = np.array(rhovapor)
zz0 = np.array(zz0) 
dd = np.array(dd)
data = np.array([temps,rholiquid,rhovapor,zz0,dd])
np.savetxt('results.dat',data.T)