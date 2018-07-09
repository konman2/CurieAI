# plots the predicted coughs compared to the tagged coughs
import matplotlib.pyplot as plt
import pickle
from Testing import Testing
import tgt
import meetings
import time

predictions = pickle.load(open('./ManuAlgoPrediction.pickle','rb'))
timeIndex = 0
timeIndexB = 0 
overlapFactor = 4
sample_interval = 3200*0.256  
pred,truth = Testing(tgt.read_textgrid('Vikram_Test_data_cough.TextGrid'),4,3200*0.256,predictions,3200)
truth = [(i[0],i[1]) for i in truth]
# creates x axis and generates all the intervals
all_times = []
x = []
for i in range(len(predictions)):
    timeIndex  += int(sample_interval/overlapFactor)
    timeIndexB  = timeIndex + sample_interval
    all_times.append((timeIndex/3200,timeIndexB/3200))
    x.append(timeIndex/3200)

#creates boolean array from the gground truth
labels_converted = []
table=meetings.make_converted_labels(all_times[::-1],truth[::-1])
for i in all_times:
    if i in table.keys():
        labels_converted.append(1.0)
    else:
        labels_converted.append(0.0)
#calculates f1 score
print(meetings.f1('./ManuAlgoPrediction.pickle','Vikram_Test_data_cough.TextGrid'))

#graphs the predcitions to the ground_truth converted
fig = plt.figure(num=None, figsize=(20, 5), facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)
plt.plot(x,predictions)
plt.plot(x,labels_converted)
plt.show()