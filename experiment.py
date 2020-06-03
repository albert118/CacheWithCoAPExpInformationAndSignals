__author__ = "Albert Ferguson"
__doc__    = "Experiment script for Information and Signals UTS."

import numpy as np  
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math
import os
import sys # used to directly call a subprocess (Python27 dependencies)
from multiprocessing import Process

################################################################################
# CONSTANTS
################################################################################

RAND_VAL             = 10                                                                               # Random seed value.
MIN_MAX_ARRIVAL_RATE = (0.5, 1.5)                                                                       # MIN and MAX of arrival rate values.
NUM_POINTS           = 10000                                                                            # Number of points to generate in linspace.
NUM_TESTS            = 6                                                                                # Number of tests to run.
LAMBDA_DELTA         = 30
ARRIVAL_RATE = np.linspace(MIN_MAX_ARRIVAL_RATE[0], MIN_MAX_ARRIVAL_RATE[1], num=NUM_POINTS)            # Generate the arrival rate linspace values.
                                                                                                        # Note: 
                                                                                                        # https://www.datacamp.com/community/tutorials/probability-distributions-python
                                                                                                        # "scale is 1/lambda in the exp. dist equation if using expon.rvs"
EXP_RAND_ARRIVAL  = stats.expon.rvs(scale=(1/ARRIVAL_RATE[0]), loc=LAMBDA_DELTA,
                                   random_state=RAND_VAL, size=NUM_POINTS)                              # Create an exponential distribution for arrival rate.
INTER_ARRIV_VALS  = [(LAMBDA_DELTA / i) for i in ARRIVAL_RATE]                                          # Inter-arrival rate, delta-lambda for incoming traffic (seconds). Array of possible values.
S_PARAM_MOMENT_1  = stats.moment(EXP_RAND_ARRIVAL, moment=2, nan_policy='raise')                        # Caclulate the 1st Moment of the distribution (Expected(X)). i.e. the Mean (note 1st moment not 0th).
NUM_NODES_MIN_MAX = (50, 120)                                                                           # The number of CoAP server nodes to generate.
NUM_NODES_VALS    = np.arange(NUM_NODES_MIN_MAX[0], NUM_NODES_MIN_MAX[1], math.ceil(
                             (NUM_NODES_MIN_MAX[1] - NUM_NODES_MIN_MAX[0])/NUM_TESTS))                  # Calculating the number of nodes to generate for testing steps.
                                                                                                        # Note: math.ceil avoids smaller steps and possible "extra" test generating.

NET_MU = 0
BIZ_MU = 0
PRO_MU = 0

def testExpRandArrival():
    # Check the values for the user...
    print('Arrival Rate Values:\t{}\n'.format(ARRIVAL_RATE))
    print('Exp. Random Dist. for Arrival Rate:\n{}\n'.format(EXP_RAND_ARRIVAL))
    print("Expected Value (1st Moment):\t{}\n".format(S_PARAM_MOMENT_1))
    # Graph the distribution...
    ax = sns.distplot(EXP_RAND_ARRIVAL, kde=True, bins=100, color='skyblue', hist_kws={"linewidth": 15,'alpha':1})
    ax.set(xlabel='Exponential Distribution', ylabel='Frequency')
    plt.show()
    del ax

def testNumNodes():
    # Check the number of nodes for the tests...
    print("Range of nodes:\t{}\n".format(NUM_NODES_MIN_MAX))
    print("Number of nodes to check and generate:\t{}\n".format(NUM_NODES_VALS))
    return

def runTests():
    testExpRandArrival()
    testNumNodes()

def TotalLayerExecTime(service_rate, lambda_x, expected_value):
    return((service_rate - lambda_x) / (expected_value + service_rate - lambda_x))

def TotalLayerServiceRate(total_layer_time, lambda_x, expected_value):
    return((total_layer_time*expected_value)/(total_layer_time+1) + lambda_x)

def setupExperiment():
    # assumes the servers have been spun up already!!
    ip       = "127.0.0.1"
    port     = 5684
    resource = "resourceA"
    python   = os.path.join("Py27Test", "Scripts", "python.exe")
    script   = os.path.join("CoAPthon", "coapclient.py")
    
    # TODO: Randomly test the servers on [min, max] ip's.
    serverproxy = "Server{}".format(str(1))
    args = '-o GET -p "coap://{}:{}/{}/{}"'.format(ip, port, serverproxy, resource)
    os.system('{} {} {}'.format(python, script, args))

setupExperiment()
