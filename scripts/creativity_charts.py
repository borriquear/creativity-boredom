#!/usr/bin/python
#print "Hello, Python!"
#Function that draws charts for creativity paper
#Figure fig:lkhratio
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math
mu1 = 4
mu2 = 6
var1 = 1
#var2 = var1
sigma = math.sqrt(var1)
x = np.linspace(0,10,100)
dist1 = mlab.normpdf(x,mu1,sigma)
dist2 = mlab.normpdf(x,mu1,sigma)*0.2
print dist1
print dist2
xindex = 0
for xi in dist1:
	if round(dist1[xi],2) == round(dist2[xi],2): xindex = xi 
print "Index is"
print xindex
plt.plot(x,mlab.normpdf(x,mu1,sigma))
plt.plot(x,mlab.normpdf(x,mu2,sigma)*0.2)
#plt.axvline(x=5,linestyle = '--',color = 'red')
plt.axvline(x=5.8,linestyle = '--',color = 'black')
plt.ylabel('Likelihood p(E|H)')
plt.xlabel('Stimulus (s)')
plt.show()
#Function that draws charts for creativity paper
#Figure fig:reactiontime
t = np.arange(0,1.1,0.1)
y0 = 0
a = 0.1
y_bear = y0 + a*t
y0 = 0.5
a2 =0.5 
y_breeze = y0 + a2*t
plt.axhline(y=1, linestyle = ':', color = 'black')
plt.plot(t, y_bear)
plt.plot(t, y_breeze)
plt.ylabel('Likelihood')
plt.xlabel('Time (t)')
plt.title('Handicaped hypothesis race')
plt.text(0.2,0.95, 'Thresdold Level')
plt.text(0.5,0.7, '$p(E|H_{Breeze})$')
plt.text(0.5,0.1, '$p(E|H_{Bear})$')
plt.text(0.82,0.85, '$p(E|H_{Breeze}=1)$')
plt.annotate('$p(H_{Breeze})$', xy=(0, 0.5), xytext=(0.05, 0.59),arrowprops=dict(facecolor='black', shrink=0.05),
            )
plt.annotate('$p(H_{Bear})$', xy=(0, 0), xytext=(0.05, 0.05),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
plt.show()





