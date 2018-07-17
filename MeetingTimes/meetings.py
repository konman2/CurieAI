# finds Overlaps between the cough predictions and the actual coughs and counts true positives
# and false positives

import time
import pickle
from Testing import Testing
import tgt
import numpy as np

#a is the first set of times
#b is the second set of times
#max_overlap is a boolean which when true returns the minimum beginning time
#and the maximum ending time
#otherwise returns the max beginning time and the minimum ending time
def overlaps(a,b,max_overlap = False,error_vals=(0,0)):
    max_end = max(a[1],b[1])
    min_end = min(a[1],b[1])
    max_beg = max(a[0],b[0])
    min_beg = min(a[0],b[0])
    #print(error_vals)
    if max(0,max_beg-error_vals[0]) <=min_end+error_vals[1] and max_end+error_vals[1] > max(0,max_beg-error_vals[0]):
        if not max_overlap:
            #return(max_beg,min_end)
            return(max(max_beg-error_vals[0],0),min_end+error_vals[1])
        #return (max(min_beg-error_val,0),max_end+error_val)
        return (min_beg,max_end)
    return(-1,-1)

#class that stores data for cough intervals
#holds a list of merged cough times
#holds a dictionary with the number of coughs that have been merged together
class Coughs:
    # a is a list of time intervals where a cough occurs
    # merges overlapping intervals and generates a dictionary with merged intervals as keys 
    # mapped to a list with all the intervals merged into the key
    # example: if [(1,7),(2,9)(3,6)] are merged an entry of (1,9): (1,7),(2,9)(3,6)] will be added to the dictionary
    def merge_overlaps(self,a,errors=(0,0)):
       
        stack = [a[0]]
        build=np.array(a[0][0])
        curr_val = 1
        a = a[1:]
        for val in a:
            inter = stack.pop()
            overlap = overlaps(val,inter,True,error_vals=errors)
            if(overlap[0]!= -1):
                stack.append(overlap)
                build = np.append(build,overlaps(val,inter)[0])
                curr_val += 1
            else: 
                stack.append(inter)
                self.num_in_overlap[inter] = build
                stack.append(val)
                curr_val = 1
                build = np.array([val[0]])
        self.num_in_overlap[stack[-1]] = build
        return stack[::-1]
        
    def __init__(self,a,thresh=(0,0)):
        self.size = len(a)

        self.num_in_overlap = {}
        # print(a)
        # print()
        self.intervals = self.merge_overlaps(a,thresh)
        # print(self.intervals,thresh)
        print()
    

# compare is the list that holds the predicted (can be merged) cough intervals
# tags is the list that holds the tagged cough intervals       
# times is a dictionary with the intervals in compare as keys which are mapped to  a list of all the time intervals
# that were merged into the interval being used as a key
# lists are sorted in descending order by the first number
# loops through the second list until the current value being compared's starting number
# is greater than the first list's end number
# After steps back to the last value that overlaps with the previous value in the first list
# then steps forward in the first list and moves forward through the second list
# If an overlap is found a binary search is done to find the closest value to the start of the overlap and
# the end of the overlap to find the number of predictions that overlap with the tag
# returns the number of overlaps found
def find_overlap(compare,tags,times):
    ind = 0
    i = 0
    last_overlap = 0
    num_overlaps = 0
    while i < len(tags) and ind < len(compare):
        val = tags[i]
        overlap = overlaps(val,compare[ind])
        if overlap[0] != -1:
            a = np.searchsorted(times[compare[ind]],overlap[0])
            b = np.searchsorted(times[compare[ind]],overlap[1]-0.256)   
            num_overlaps+=max(0,b-a)+1
            last_overlap = i
            
            # if a<times[compare[ind]].size and b<times[compare[ind]].size:
            #     print(overlap,compare[ind],a,b,times[compare[ind]][a],times[compare[ind]][b])
            # else:
            #     print(overlap,compare[ind],a,b)
        elif overlap[0] == -1 and val[0]<compare[ind][1]:
            ind+=1
            i = last_overlap-1 
        i+=1
    return num_overlaps 

# makes a list of converted labels from the ground truth coughs to be graphed
# to see how algorithm works look at find_overlap
# compare must be a list of every time interval
# tags the list of manually tagged coughs
def make_converted_labels(compare,tags,min_size=0):
    ind = 0
    i = 0
    last_overlap = 0
    table = {}
    while i < len(tags) and ind < len(compare):
        val = tags[i]
        overlap = overlaps(val,compare[ind])
        if overlap[0] != -1:
            if val[1]-val[0] >=min_size:
                table[tuple(compare[ind])] = 1
            last_overlap = i
        elif overlap[0] == -1 and val[0]<compare[ind][1]:
            ind+=1
            i = last_overlap-1
        i+=1
    return table 

def delete_vals(compare,tags):
    ind = 0
    i = 0
    last_overlap = 0
    table = {}
    while i < len(tags) and ind < len(compare):
        val = tags[i]
        overlap = overlaps(val,compare[ind])
        if overlap[0] != -1:
            #print(compare[ind],val)
            del compare[ind]
            i-=1
            last_overlap = i
        elif overlap[0] == -1 and val[0]<compare[ind][1]:
            ind+=1
            i = last_overlap-1
        i+=1
    return compare 
        
#preds is a pickle file with a boolean array of predictions
#grid_file is a TextGrid file with tagged data
#error_val is the accepted error value to match an overlap; default is 0
#the error_val is multiplied by 2 so a parameter of 0.5 will yield an error value of 0.5 forward
# and 0.5 backwards so the total error_value will be 1.0
#returns false_positives and true_positives in that order if for_pos is True (default)
#returns false_negatives and true_negatives in that order if for_pos is False
def find(vals,error_vals=(0,0),for_pos=True):
    predictions = Coughs([(i[0],i[1]) for i in vals[0]],error_vals)
    tags = Coughs([(i[0],i[1]) for i in vals[1]])
    over = find_overlap(predictions.intervals,tags.intervals,predictions.num_in_overlap)
    if for_pos:
        return(predictions.size-over,over,predictions.intervals)
    return(over,predictions.size-over)
    
# calculates f1 score by running overlap function with two different data sets from Testing function
# one to count false vs true positives and one to count false vs true negatives
def f1(predictions,grid_file,error=(0,0)):
    #Testing(grid_file,cre4,3200*0.256,pred,3200,for_pos)
    vals = Testing(tgt.read_textgrid(grid_file),4,32000*0.256,pickle.load(open(predictions,'rb')),32000,for_pos=False)
    false_pos,true_pos,merged_pos=find(Testing(tgt.read_textgrid(grid_file),4,32000*0.256,pickle.load(open(predictions,'rb')),32000,True),error)
    if error != (0,0):
        vals = (delete_vals(vals[0],merged_pos),vals[1])
   
   
    false_neg,true_neg=find(vals,(0,0),for_pos=False)
    #false_neg = true_neg = 1
    print(false_pos,true_pos,false_neg,true_neg)
    precision = true_pos/(true_pos+false_pos)
    recall = true_pos/(true_pos+false_neg)
    print(precision,recall)
    
    score = 2*(precision*recall/(precision+recall))
    print(score)
    return merged_pos