"""
Created on Thu Jan 25 15:16:43 2018
Author: Ian Taulli
Discription:
"""
import numpy as np
import matplotlib.pyplot as plt

def modtest(x):
    j=0
    for i in range(x+1):
        j+=i
    return j