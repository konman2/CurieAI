import librosa
import matplotlib.pyplot as plt
from librosa import display
import pickle
from Testing import Testing
import tgt
import meetings
predictions = pickle.load(open('./ManuAlgoPrediction.pickle','rb'))
timeIndex = 0
timeIndexB = 0 
overlapFactor = 4
sample_interval = 3200*0.256  
pred,truth = Testing(tgt.read_textgrid('Vikram_Test_data_cough.TextGrid'),4,3200*0.256,predictions,3200)
truth = [(i[0],i[1]) for i in truth]
t = []
x = []
for i in range(len(predictions)):
    timeIndex  += int(sample_interval/overlapFactor)
    timeIndexB  = timeIndex + sample_interval
    t.append((timeIndex/3200,timeIndexB/3200))
    x.append(timeIndex/3200)

labels_converted = []
for i in t:
    overlap = False
    for j in truth:
        if meetings.overlaps(i,j)[0]!= -1:
            labels_converted.append(1.0)
            overlap = True
            break
    if not overlap:
        labels_converted.append(0.0)

#print(t)
fig = plt.figure(num=None, figsize=(20, 5), facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)
plt.plot(x,predictions)
plt.plot(x,labels_converted)
plt.show()