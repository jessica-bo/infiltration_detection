"""
Created on February 19, 2020 by jessica-bo
Algorithm from https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/56451135#56451135

"""

import numpy as np
import time
from pylab import *

import matplotlib.pyplot as plt

from peakdetector import PeakDetector


y = np.array(np.loadtxt(fname = "data/thin-wire-18-infiltration-3.txt"))

#lag = the lag of the moving window for smoothing
lag = 10
#threshold = the z-score at which the algorithm signals
threshold = 5
#influence = the influence (between 0 and 1) of new signals on the mean and standard deviation
#   e.g. 0 assumes that the signal average is always stationary
influence = 0.01


"""
Non real-time version

"""
peak = PeakDetector(array=y, lag=lag, threshold=threshold, influence=influence)

# Run algo with settings from above
result = PeakDetector.thresholding_algo(peak)

peaktime = PeakDetector.extractpeaktime(result["signals"])

fig, axes = plt.subplots(2, 1, sharex=True, sharey=False)
ax = axes.ravel()
fig.suptitle("Infiltration Spike Detection", fontsize=18)

ax[0].plot(np.arange(1, len(y)+1), y, linewidth=3, color='k', label="Signal")
ax[0].plot(np.arange(1, len(y)+1), result["avgFilter"], color='b', linewidth=1)
ax[0].plot(np.arange(1, len(y)+1),
           result["avgFilter"] + threshold * result["stdFilter"], color='g', linewidth=1)
ax[0].plot(np.arange(1, len(y)+1),
           result["avgFilter"] - threshold * result["stdFilter"], color='g', linewidth=1)
ax[0].set_ylim([0, max(y)*1.2])
ax[0].set_ylabel("Impedance", fontsize=14)

ax[1].plot(np.arange(1, len(y)+1), result["signals"], color="r", linewidth=2)
if peaktime is not None: 
    ax[1].axvline(x=peaktime, linestyle='--', color='b', linewidth=1)
    ax[1].text(peaktime+2,1.5,"Time = %.1f s" % peaktime, fontsize=10, color='b')
ax[1].set_ylim([-2,2])
ax[1].set_ylabel("Signal", fontsize=14)


fig.tight_layout()
plt.savefig("detectedpeak.png", facecolor='w', edgecolor='none')
plt.show()


"""
Real-time version

"""

#y_reduced = y[0:lag]
#
#peak = PeakDetector(array=y_reduced, lag=lag, threshold=threshold, influence=influence)
#result = PeakDetector.thresholding_algo(peak)
#
#signal = result['signals']
#
#for num in y[lag::]:
##    print("New reading: %f" % num)
##    time.sleep(.01)
#    reading = PeakDetector.realtime_thresholding_algo(peak, num)
#    signal = np.append(signal, reading)
#    
#    
## Plotting     
#fig, ax1 = plt.subplots()
#t = np.arange(0,len(y))
#
#color = 'tab:blue'
#ax1.set_xlabel('time (s)')
#ax1.set_ylabel('exp', color=color)
#ax1.plot(t, y, color=color)
#ax1.tick_params(axis='y', labelcolor=color)
#
#ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#
#color = 'tab:red'
#ax2.plot(t, signal, color=color, linewidth=1)
#ax2.tick_params(axis='y', labelcolor=color)
#
#fig.tight_layout()  # otherwise the right y-label is slightly clipped
#plt.show()

