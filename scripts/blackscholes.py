#!/usr/bin/python
from sympy import *
from scipy import stats
import math
import numpy as np
import matplotlib.pyplot as plt
def black_scholes (cp, s, k, t, v, rf, div):
        """ Price an option using the Black-Scholes model.
        s: initial stock price
        k: strike price
        t: expiration time
        v: volatility
        rf: risk-free rate
        div: dividend
        cp: +1/-1 for call/put
        """

        d1 = (math.log(s/k)+(rf-div+0.5*math.pow(v,2))*t)/(v*math.sqrt(t))
        d2 = d1 - v*math.sqrt(t)

        optprice = (cp*s*math.exp(-div*t)*stats.norm.cdf(cp*d1)) - (cp*k*math.exp(-rf*t)*stats.norm.cdf(cp*d2))
        return optprice
	print " Print"
	print optprice

def black_scholes_hedonic (k, final_time, v):
        """ Price an option using the Black-Scholes model.
        s: pred_pleasure -- initial stock price
        pred_error --inverse of  pred_pleasure 
        k: boredom constant --strike price
        t: expiration time
        v: sigma -- volatility
	#meas_error = 
        """
	t = np.arange(0.0,final_time,0.1)
	# calculate P (Prediction) component
	#mean and standard deviation of the measurement error
	#prediction error and mesurement error are different, meas_error can not be eliminated, prediction error you can if perfect predictions
	mu_error = 0
	sigma_error = 0.01   
	meas_error = np.random.normal(mu_error, sigma_error, len(t))
	pred_error = np.exp(-t/v + meas_error)
	#pred_error_prime = pred_error.diff(t)
	pred_error_prime = np.exp(-t/v) 
	#t = Symbol('t') 
	#pred_error = np.exp(-t/v) 
	pred_pleasure = 1/pred_error
	s = pred_pleasure
	rf = pred_error_prime
        d1 = (np.log(s/k)+(rf+0.5*np.power(v,2)))/(v)
        d2 = d1 - v
	print "Prediction error is:"
	print pred_error
	print "Prediction pleasure is:"
	print pred_pleasure
	pred_error_price = []
	pred_pleasure_price = []
	d2list = []
	d1list = []
	d2list_boredom = []
	for i in xrange(len(d1)):
		d2_element = stats.norm.cdf(d2[i])
		d1_element = stats.norm.cdf(d1[i])
		#x = np.asarray(pred_error[i])*np.asarray(d2_element) 
		#y = np.asarray(pred_pleasure[i])*np.asarray(d2_element) 
		x = np.asarray(pred_error[i])*np.asarray(d2_element) 
		y = np.asarray(pred_pleasure[i])*np.asarray(d1_element) 
		pred_error_price.append(x)
		pred_pleasure_price.append(x)
		d2_boredom_element = 1 - d2_element
		d2list.append(d2_element)
		d1list.append(d1_element)
		d2list_boredom.append(d2_boredom_element)
	print "d1 prob of P"
	print d1list
	print "d2 prob of  B"
	print d2list
	print "pred_error"
	print pred_error
	print "error price"
	print pred_error_price
	print "pred pleasure"
	print pred_pleasure
	print "pleasure price"
	print pred_pleasure_price
	error_line, = plt.plot(t,pred_error, 'r', label = "e")
	error_legend = plt.legend(handles=[error_line], loc=1)
	ax = plt.gca().add_artist(error_legend)
	s_line, = plt.plot(t,pred_pleasure, 'g', label = "s")
	s_legend = plt.legend(handles=[s_line], loc=2)
	ax = plt.gca().add_artist(s_legend)
	d2_line, = plt.plot(t,d2list, 'r--', label = "p(d2)")
	d2_legend = plt.legend(handles=[d2_line],loc=3)
	ax = plt.gca().add_artist(d2_legend)
	pleasure_line, = plt.plot(t,pred_pleasure_price, 'g--', label = "(s*d2)")
	pleasure_legend = plt.legend(handles=[pleasure_line],loc=4)
	ax = plt.gca().add_artist(pleasure_legend)
	plt.suptitle(' V = P - B')
	plt.xlabel('time')
	plt.ylabel('prediction/pleasure error')
	k_list = [k]*len(d2list)	
	k_fact_list = k/rf
	boredom_line, = plt.plot(t,k_fact_list, 'y')
	boredom_legend = plt.legend(handles=[boredom_line], loc=5)	
	ax = plt.gca().add_artist(boredom_legend)
	k_list = [k]*len(d2list)	
	# calculate B (Boredom) component
	boredom = np.maximum(k_fact_list, k_list) 
	#boredom_fact = boredom*d2list_boredom
	boredom_fact = boredom*d2list
	# Subjective value to maximize
	subjective_value = pred_pleasure_price - boredom_fact
	print " boredom"
	print boredom
	print " boredom fact"
	print boredom_fact
	print " subjecive value"
	print subjective_value
	boredom_bound_line, = plt.plot(t,boredom, 'c', label = "B")
	boredom_bound_legend = plt.legend(handles=[boredom_bound_line], loc=6)
	ax = plt.gca().add_artist(boredom_bound_legend)
	boredom_fact_line, = plt.plot(t,boredom_fact, 'c--', label = "B*(1-d2)")
	boredom_fact_legend = plt.legend(handles=[boredom_fact_line],loc =7)
	ax = plt.gca().add_artist(boredom_fact_legend)
	v_line, = plt.plot(t,subjective_value, linewidth= 3 , c="black",label = "V") 
	v_legend = plt.legend(handles=[v_line],loc=8)
	ax = plt.gca().add_artist(v_legend)
	plt.show()
 
k=10
final_time = 100
v= 2
black_scholes_hedonic (k, final_time, v)