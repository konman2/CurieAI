import matplotlib.pyplot as plt
import pickle
from Testing import Testing
import tgt
import meetings
import time
#from show import x
import librosa

y,sr = librosa.core.load("Vikram_Test_data_cough.wav",sr=32000)
print(len(y),sr)
for i in y:
    if i != 0:
        print(i)
#plt.plot(y)
#plt.show()

# for i in range(len(predictions)):
#     timeIndex  += int(sample_interval/overlapFactor)
#     timeIndexB  = timeIndex + sample_interval
#     all_times.append((timeIndex/
# all_times = []
# stack = []
# def create_labels(table):
#     labels_converted = []
#     for i in all_times:
#         if i in table.keys():
#             labels_converted.append(1.0)
#         else:
#             labels_converted.append(0.0)
#     return labels_converted

# def print_real_time(sample_interval,overlapFactor,desiredFs,pred,count,threshhold=(0,0),min_size=0):
    
#     for c,i in enumerate(pred):
#         val = ((count+c+1)*int(sample_interval/overlapFactor),(count+c+1)*int(sample_interval/overlapFactor)+sample_interval)
#         all_times.append(val)
#         if i == 1.0:
#             if len(stack) != 0:
#                 inter = stack.pop()
#                 overlap = meetings.overlaps(val,inter,True,error_vals=threshhold)
#                 if(overlap[0]!= -1):
#                     stack.append(overlap)
#                 else: 
#                     stack.append(inter)
#                     stack.append(val)
#             else:
#                 stack.append(val)
#     predictions = create_labels(meetings.make_converted_labels(all_times[::-1],stack[::-1],min_size))
#     #print(predictions)
#     plt.plot(predictions)
#     plt.draw()

# p = predictions = pickle.load(open('./ManuAlgoPrediction.pickle','rb'))
# plt.ion()
# for c,i in enumerate(p):
#     print(i)
#     print_real_time(32000*0.256,4,32000,[i],c,(0.25,0.25),0)
#     plt.pause(0.01)
# plt.show()

