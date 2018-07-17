# plots the predicted coughs compared to the tagged coughs
import matplotlib.pyplot as plt
import pickle
from Testing import Testing
import tgt
import meetings
import time
import librosa as lib
from scipy.io import wavfile
import numpy as np

predictions = pickle.load(open('./ManuAlgoPrediction.pickle','rb'))
timeIndex = 0
timeIndexB = 0 
overlapFactor = 4
sample_interval = 32000*0.256  
desiredFs=320000
pred,truth = Testing(tgt.read_textgrid('Vikram_Test_data_cough.TextGrid'),4,32000*0.256,predictions,32000)
truth = [(i[0],i[1]) for i in truth]

error = (0.25,0.25)
min_size=0.
# creates x axis and generates all the intervals
all_times = []
x = []
for i in range(len(predictions)):
    timeIndex  += int(sample_interval/overlapFactor)
    timeIndexB  = timeIndex + sample_interval
    all_times.append((timeIndex/32000,timeIndexB/32000))
    x.append(timeIndex/32000)

#creates boolean array from the gground truth


def create_labels(table):
    labels_converted = []
    for i in all_times:
        if i in table.keys():
            labels_converted.append(1.0)
        else:
            labels_converted.append(0.0)
    return labels_converted

labels_converted = create_labels(meetings.make_converted_labels(all_times[::-1],truth[::-1]))
start = time.time()
merged_pos = meetings.f1('./ManuAlgoPrediction.pickle','Vikram_Test_data_cough.TextGrid',error)
end = time.time()

if error != (0,0) or min_size != 0:
    predictions = create_labels(meetings.make_converted_labels(all_times[::-1],merged_pos,min_size))

#calculates f1 score

def delete_dwarfs(min_size):
    curr_count = 0
    
    start_one = 0
    for i,val in enumerate(predictions):
        if val == 1.0:
            curr_count+=1
            if start_one == 0:
                start_one = i
        else:
            if curr_count != 0 and curr_count<min_size:
                predictions[start_one:i]  = [0.0 for j in range(i-start_one)]
            # elif (curr_count>= min_size):
            #     print("here")
            curr_count = 0
            start_one=0
        
#delete_dwarfs(10)

#graphs the predcitions to the ground_truth converted
fig = plt.figure(num=None, figsize=(20, 5), facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

plt.plot(x,predictions)
# plt.ion
# a = []
# for i  in predictions:
#     a.append(i)
#     plt.plot(x[0:len(a)],a)
#     plt.draw()
#     plt.pause(0.01)
# plt.show(block=True)
#plt.plot(x,labels_converted,'r.')

# fs, data_to_play = wavfile.read("Vikram_Test_data_cough.wav") # read in the audio file, fs : frequency sampling : 44.1k 48k, 32k Hz . 
# data_to_play = np.float32(data_to_play) # cast to float 32 bit
# dataSR = lib.resample(data_to_play, fs, desiredFs) # resampling to 32k Hz
# data_to_playNorm = dataSR/np.max(dataSR) # normalize data between -1 and 1
y,sr = lib.core.load("Vikram_Test_data_cough.wav",sr=32000)
#plt.plot(data_to_playNorm)
lib.display.waveplot(y,sr=sr)
# print(y,sr)
# plt.plot(y)
plt.show()
#plt.draw()
# for i in range(merged_pos):
#     print(i,merged_pos[i])

#plt.show()

