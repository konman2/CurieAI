import time
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
class Person:
    #not sure if neccesary. Merges overlapping time frames from the same person
    def merge_overlaps(self,a):
        stack = []
        for val in reversed(a):
            if len(stack) == 0:
                stack.append(val)
            inter = stack.pop()
            overlap = overlaps(val,inter,True)
            if(overlap[0]!= -1):
                stack.append(overlap)
            else:
                stack.append(inter)
                stack.append(val)
        
        return stack[::-1]
        
    def __init__(self,a):
        self.intervals = sorted(a,key=get_key,reverse=True)
        #maybe needed
        #self.intervals = self.merge_overlaps(self.intervals)
#lists are sorted in descending order by the first number
#loops through second list until the current value being compared in the first list end number
# is greater than the first lists end number
#After takes one step back to the last value that overlaps with the previous
#value in the first list, then steps forward in the first list and moves forward through the second list
def find_overlap(meeting_times):
    #tart = time.time()
    ind = 0
    compare = meeting_times[0].intervals
    i = 0
    last_overlap = 0
    while i < len(meeting_times[1].intervals) and ind < len(compare):
        val = meeting_times[1].intervals[i]
        last_val = False
        overlap = overlaps(val,compare[ind])
        #print(ind,i,compare[ind],val)
        if i == len(meeting_times[1].intervals)-1: 
            ind+=1
            i = last_overlap-1
            last_val = True
        if overlap[0] == -1 and not last_val  and val[1]<compare[ind][1]:
            ind+=1
            i = last_overlap-1
        if overlap[0] != -1:
            #print(ind,i,compare[ind],val,,overlap)
            last_overlap = i
        i+=1
    #end = time.time()
    #return end-start

def run():
    file = open("./test.txt")
    meeting_times = [] 
    temp = []
    tot_time = 0 
    # file IO to read in data
    for l in file.readlines():
        if len(l) > 1:
            #print(l)
            a = (int(l[:l.find(' ')]),int(l[l.find(' ')+1:]))
            temp.append(a)
        else:
            #tot_time = time.time()
            meeting_times.append(Person(temp))
            #tot_time = time.time()-tot_time
            temp = []
    # start = time.time()
    # meeting_times.append(Person(temp))
    # tot_time = time.time()-start
    #tot_time+=find_overlap(meeting_times)
    #return tot_time
    find_overlap(meeting_times)
#print(meeting_times[0].intervals,meeting_times[1].intervals)
run()