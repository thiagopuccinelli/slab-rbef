import numpy as np 
import matplotlib.pyplot as plt 
from scipy import interpolate
from scipy.optimize import curve_fit

def func1(x,C,B):
    return C*x + B 

def func2(x,C,B):
    return x/C - B/C 

def func(x,a,b):
    return a*x**2 + b


data = np.genfromtxt("results.dat")

beta = 0.325
rhol = data[:,1]
rhov = data[:,2]
temps = data[:,0]

# plt.figure()
y = rhol - rhov 
y = y ** (1./beta)
#plt.plot(temps, y)
popt,pcov = curve_fit(func1,temps, y)
#print(popt)
C = popt[0]
B = popt[1]
Tc = - B / C 
# plt.show()

# plt.figure()
y = 0.5*(rhol + rhov)
popt,pcov = curve_fit(func1,Tc-temps,y)
B = popt[1]
C = popt[0]
rhoc = B 
#plt.plot(temps,y-C*(Tc-temps), marker="o")
# plt.show()
print(Tc, rhoc)

plt.figure()
rho = np.concatenate((data[:,2],[rhoc],np.flip(data[:,1])))
newT = np.concatenate((data[:,0],[Tc],np.flip(data[:,0])))

plt.plot(rho,newT,marker="o",ms="7.5",ls="none",color="red")
tck,u = interpolate.splprep([rho, newT], s=0)
unew = np.arange(0, 1.01, 0.01)
out = interpolate.splev(unew, tck)
plt.plot(out[0], out[1],'-',color="black",lw=2)

plt.text(0.2, 0.7, r'V + L', fontsize = 22)
plt.text(0., 1.2, r'V', fontsize = 22)
plt.text(0.8, 1.2, r'L', fontsize = 22)
plt.text(0.22, 1.25, r'$\rho_c$,$T_c$', fontsize = 18)

plt.ylim(0.3,1.5)
plt.xlim(-0.1,1)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.minorticks_on()
plt.xlabel(r"$\rho$",fontsize=22)
plt.ylabel(r"$T$",fontsize=22)
plt.tight_layout()
plt.savefig("phase-diagram.pdf")
plt.show()