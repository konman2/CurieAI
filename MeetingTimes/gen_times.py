from random import randint
import meetings
import matplotlib.pyplot as plt
import math
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

def merge_overlaps(a):
    a = sorted(a)
    stack = []
    for val in a:
        if len(stack) == 0:
            stack.append(val)
        inter = stack.pop()
        overlap = overlaps(val,inter,True)
        if(overlap[0]!= -1):
            stack.append(overlap)
        else:
            stack.append(inter)
            stack.append(val)
    
    return stack

def create(person,size):
    for i in range(0,size):
        a = randint(randint(1,9900),10000)
        b = randint(a+1,a+10)
        person.append((a,b))
    return person


def write(person,f):
    for i in person:
        f.write(str(i[0])+ " " +str(i[1]))
        f.write("\n")
    f.write("\n")


def get_time():
    f = open("test.txt","w")
    sizes = [100,200,300,400,500,1000,1500,2500,2000,3000,4000,5000,6000,600,700,10000,50000,100000]
    times = []
    for ci,i in enumerate(sizes):

        person1 = []
        person2 = []
        person1 = create(person1,i)
        person2 = create(person2,i)
        person1 = merge_overlaps(person1)
        person2 = merge_overlaps(person2)
        f = open("test.txt","w")
        write(person1,f)
        write(person2,f)
        f.close()
        #sizes[ci] = math.log(len(person1)+len(person2))/math.log(2)
        sizes[ci] = len(person1)+len(person1)
        t = 0.0
        x = []
        for i in range(0,10):
            a = meetings.run()
            x.append(a)
            t+= a
        t/=len(x)
        #times.append(meetings.run())
        times.append(t)
    print(sizes)
    print(times)
    plt.plot(sizes,times,'ro')
    plt.show()
get_time()



