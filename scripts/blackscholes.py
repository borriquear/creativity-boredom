#!/usr/bin/python
from sympy import *
from scipy import stats
import math
import os.path
import numpy as np
import matplotlib
import matplotlib.artist as artists
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

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
    #print " Print"
    #print optprice

def black_scholes_hedonic (p0, k, final_time, v, r):
    """ Price an option using the Black-Scholes model.
        p0: initial pred_pleasure -- initial stock price
        k: boredom constant --strike price
        final_time: expiration time
        v: sigma -- volatility
        r: pedictability ration of the external world. k(w)/w = 1 totally random world, r = 0 totally pedictable
    """    
    #time vector    
    t_slots = 0.001
    t = np.arange(0.0,final_time,t_slots)
    mu_error = 0.0
    sigma_error = v
    #meas_error = np.random.normal(mu_error, sigma_error, len(t))
    #pred_error = np.exp(-t/v + meas_error)
    #pred_error_prime = np.exp(-t/v) #pred_error_prime = pred_error.diff(t)
    #mean of the logarithm of predictio error
    std_pred_error = sigma_error*np.sqrt(final_time - t)
    std_pred_pleas = std_pred_error
    mean_pred_error = (mu_error - np.power(sigma_error,2)*0.5)*(final_time - t)
    mean_pred_pleas = (-mu_error + np.power(sigma_error,2)*0.5)*(final_time - t)
    #monte carlo sample of the log prediction pleasure
    mc_pred_pleas_log = np.random.normal(np.log(p0) + mean_pred_pleas, std_pred_pleas)
    mc_pred_pleas = np.log(p0) + np.exp(mean_pred_pleas)
    mc_pred_pleas_t =  np.exp(mc_pred_pleas_log)
    boredom_pain= k*np.exp(-r*(final_time - t))
    print "std_pred_pleas"
    print std_pred_pleas
    print " mc_pred_pleas_log .."
    print mc_pred_pleas_log
    print " mc_pred_pleas .."
    print mc_pred_pleas
    print "mc_pred_pleas_t"
    print mc_pred_pleas_t
    
    #return
    
    #d1 = (np.log(mc_pred_pleas/k) + (r + 0.5*np.power(v,2))*(final_time - t))/(v*np.sqrt(final_time - t))
    #d2 = (np.log(k/mc_pred_pleas) + (r - 0.5*np.power(v,2))*(final_time - t))/(v*np.sqrt(final_time - t))
    #d1 = (np.log(mc_pred_pleas/k) - (r + 0.5*np.power(v,2))*(final_time - t))/(v*np.sqrt(final_time - t))
    #d2 = 1 - d1
    d2 = (np.log(k/mc_pred_pleas) + (-r + 0.5*np.power(v,2))*(final_time - t))/(v*np.sqrt(final_time - t))
    #d1 = 1 - d2    
    pred_pleasure_price = []    
    boredom_pain_price = []
    subjective_experience_price = []
    d1list = [] 
    d2list = []
    for i in xrange(len(d2)):
        #d1_element = stats.norm.cdf(d1[i])
        d2_element = stats.norm.cdf(d2[i])
        d1_element = 1 - d2_element
        d1list.append(d1_element)
        d2list.append(d2_element)
        pred_pleas_w = np.asarray(mc_pred_pleas[i])*np.asarray(d1_element)
        boredom_w = (np.asarray(boredom_pain[i]))*np.asarray(d2_element)  
        subjective_experience_w = pred_pleas_w - boredom_w
        pred_pleasure_price.append(pred_pleas_w)
        boredom_pain_price.append(boredom_w)   
        subjective_experience_price.append(subjective_experience_w)
    print "d1 prob of P"
    print d1list
    print "d2 prob of  B"
    print d2list
    print "pred_pleasure_price"
    print pred_pleasure_price
    print "boredom_pain_price"
    print boredom_pain_price
    print "subjective_experience_price"
    print subjective_experience_price
    #Charts
    #plt.plot(t,pred_pleasure_price,'g--', label = "p")
    #plt.plot(t,boredom_pain_price,'y', label = "b") 
    #plt.plot(t,subjective_experience_price,'b', label = "v")
    fig=plt.figure(1)  
    ax = plt.subplot(111)
    ax.plot(t, d1list, 'g--', label = "$N(d_{1})$")
    ax.plot(t, d2list, 'r--', label = "$N(d_{2})$")
    ax.plot(t, pred_pleasure_price, 'g', label = "$Prediction (p)$")
    ax.plot(t, boredom_pain_price, 'r', label = "$Boredom (b)$")
    ax.plot(t, subjective_experience_price, 'b', label = "$Experience (v)$")
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=3)
    plt.title('$r = %.1f $' %r)
    plt.title('$p_0/k = %.2f$' %ratiopk, loc='left')
    plt.title('$v = p - b$', loc='right')
    ax.set_xlabel('$t$')
    ax.set_ylabel('$value$')   
    plt.show()
    figures_path = 'c:/workspace/github/figures'
    base_filename = 'r0-u0v1-p1k1'
    filename_suffix = 'png'
    dest_file = os.path.join(figures_path, base_filename + "." + filename_suffix)
    fig.savefig(dest_file, dpi=600, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

final_time = 1
v= 1.0
r = 0.0
p0 = 1.0
k = 1.0
ratiopk = p0/k
black_scholes_hedonic (p0, k, final_time, v, r)