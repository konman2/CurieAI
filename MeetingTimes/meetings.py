import time
import pickle
from Testing import Testing
import tgt
#algorithm to find possible meeting times between two people
def get_key(i):
    return i[0]

def overlaps(a,b,max_overlap = False):
    max_end = max(a[1],b[1])
    min_end = min(a[1],b[1])
    max_beg = max(a[0],b[0])
    min_beg = min(a[0],b[0])
    if max_beg <= min_end and max_end > max_beg:
        if not max_overlap:
            return(max_beg,min_end)
        return (min_beg,max_end)
    return(-1,-1)
class Coughs:
    #not sure if neccesary. Merges overlapping time frames from the same person
    def merge_overlaps(self,a,table):
        stack = []
        curr_val = 1
        for val in reversed(a):
            if len(stack) == 0:
                stack.append(val)
            inter = stack.pop()
            overlap = overlaps(val,inter,True)
            if(overlap[0]!= -1):
                stack.append(overlap)
                curr_val += 1
            else:
                stack.append(inter)
                table[inter] = curr_val
                stack.append(val)
                curr_val = 0
        table[stack[len(stack)-1]] = curr_val
        return stack[::-1],table
        
    def __init__(self,a):
        self.intervals = sorted(a,key=get_key,reverse=True)
        #maybe needed
        self.intervals,self.num_in_overlap = self.merge_overlaps(self.intervals,{})
        
        
#lists are sorted in descending order by the first number
#loops through second list until the current value being compared in the first list end number
# is greater than the first lists end number
#After takes one step back to the last value that overlaps with the previous
#value in the first list, then steps forward in the first list and moves forward through the second list
def find_overlap(meeting_times):
    ind = 0
    compare = meeting_times[0].intervals
    i = 0
    last_overlap = 0
    table = {}
    while i < len(meeting_times[1].intervals) and ind < len(compare):
        val = meeting_times[1].intervals[i]
        last_val = False
        overlap = overlaps(val,compare[ind])
        #print(ind,i,compare[ind],val)
        if overlap[0] != -1:
            #print(overlap)
            table[compare[ind]] = val
            meeting_times[0].num_in_overlap[compare[ind]] += meeting_times[1].num_in_overlap[val]
            last_overlap = i
        if i == len(meeting_times[1].intervals)-1: 
            ind+=1
            i = last_overlap-1
            last_val = True
        if overlap[0] == -1 and not last_val  and val[1]<compare[ind][1]:
            ind+=1
            if last_overlap != 0:
                i = last_overlap-1
            else:
                i-=1
       
        i+=1
    return table

def find(predictions,grid_file,error_val=0):
    file = open("./test.txt")
    pred = pickle.load(open(predictions,'rb'))
    vals = Testing(tgt.read_textgrid(grid_file),4,3200*0.256,pred,3200)
    predictions = [(max(0,i[0]-error_val),i[1]+error_val) for i in vals[0]]
    tags = [(i[0],i[1]) for i in vals[1]]
    meeting_times = [Coughs(predictions),Coughs(tags)]      
    # file IO to read in data
    table = find_overlap(meeting_times)
    # print(meeting_times[0].intervals)
    # print(len(meeting_times[0].intervals))
    # print(meeting_times[1].intervals)
    false_pos = 0
    true_pos = 0
    for i in meeting_times[0].intervals:
        if  i not in table.keys():
            false_pos+=meeting_times[0].num_in_overlap[i]
            print(i)
        else:
            true_pos+=meeting_times[0].num_in_overlap[i]
    print(false_pos)
    print(true_pos)
    

#print(meeting_times[0].intervals,meeting_times[1].intervals)
#find('./ManuAlgoPrediction.pickle','Vikram_Test_data_cough.TextGrid',0)