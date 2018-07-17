# this function test the FNN model on streamign data, this is for cough data
# numFeatures = 168
# overlapFactor = 4 (75% overlap or 1/4 hop size )
# oneSegLen = 8192 (256 ms at 32000 khz)
# threshold is used to decide what is the label, usually anything more than 0 is the label,anything above 0 will make it more restrict.
# predictions is a boolean vectore
# features : test feature matrix
# return accuracy and false alarm 
# Modules needed for this code:
import numpy as np
import tensorflow as tf
import pickle
import IPython.display
import sklearn
import librosa as lib
import librosa.display
from sklearn import preprocessing
import time
import numpy as np
import scipy
from scipy.io import wavfile
from scipy import ndimage
#from Decoder import random_mini_batches
import time
import pylab as pl
import tgt
#from Inference import predict
import sys
import matplotlib.pyplot as plt


def Testing(TextGrid, overlapFactor, sample_interval, predictions, desiredFs,for_pos=True):

    # read in the ground truth
    tg = TextGrid
    Labels_Time_Interval = tg.tiers
    sizeLabels = np.shape(Labels_Time_Interval)
    startTimes = []
    endTimes = []
    TrueLabels = []
    groundinfo = []
    test= []
    for i in range(0,sizeLabels[1]): #getting labeled data
        interval1 = Labels_Time_Interval[0][i]
        startTimes.append(float(interval1.start_time))
        endTimes.append(float(interval1.end_time))
        TrueLabels.append(interval1.text)
        groundinfo.append([float(interval1.start_time),float(interval1.end_time)])

    #######


    timeIndex = 0
    total_count = 0
    countRight = np.zeros((len(startTimes),1))
    countFalse = np.zeros((len(predictions),1))
    index =0
    start = 0
    end = 0
    index = 0
    i = 0
    predictedStmaps = []
        
    timeIndex = 0
    timeIndexB = 0
    for i in range(len(predictions)):
            timeIndex  += int(sample_interval/overlapFactor)
            timeIndexB  = timeIndex + sample_interval
            if predictions[i] == for_pos:    
                predictedStmaps.append([round((timeIndex)/desiredFs,6),round((timeIndexB)/desiredFs,6)])
    return (predictedStmaps ,groundinfo)