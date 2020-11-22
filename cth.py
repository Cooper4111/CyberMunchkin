'''
This file is used to visualize hitchance cap mechanics
For developer purposes only
'''

import matplotlib.pyplot as plt
import numpy as np

sqrt = lambda x: x**(0.5)

def cth(delta, baseCth = .5**(.5), ret = 'coeff'):
    delta /= 100
    cth1 = baseCth * (1+delta)**(-0.5)
    cth2 = min(1, baseCth * (1+delta)**(0.5))
    if ret == 'cth1':
        return cth1
    elif(ret == 'cth2'):
        return cth2
    else:
        return cth2 / cth1
    
def derivetive(val, funk, h = 0.001):
    a = funk(val+h)
    b = funk(val)
    return (a - b) / h

vf = np.vectorize(cth)
baseCth = 0.7
deltaLim = 500

rng = np.arange(0,deltaLim)
plt.plot(rng, vf(rng), label = 'base = ~0.7')
plt.plot(rng, vf(rng, 0.8), label = 'base = 0.8')
plt.plot(rng, vf(rng, 0.5), label = 'base = 0.5')
plt.plot(rng, vf(rng, 1/sqrt(2+1)), label = 'base = test')
plt.grid()
plt.yticks(np.arange(0,4,.25))
plt.legend(loc='lower right')

plt.show()
#plt.clf()

der = np.vectorize(derivetive)

plt.plot(np.arange(0,deltaLim), der(np.arange(0,deltaLim), cth)*100)
#plt.yticks(range(0,20,2))
plt.grid()
#plt.show()


print(cth(100, ret='cth2'))