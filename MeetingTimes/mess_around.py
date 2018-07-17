import matplotlib.pyplot as plt
from random import randint



tot = []
for i in range(100):
    l = []
    for i in range(10):
        if randint(1,10) == 1:
            l.append(1.0)
        else:
            l.append(0.0)
    tot.append(l)
b = [0.0,0.0]

# plt.plot(l)
# plt.show()
plt.ion()
t = []
for i in range(100):
    
    for i in range(10):
        if randint(1,2) == 1:
            t.append(1.0)
        else:
            t.append(0.0)
    
    plt.plot(t)
    # print(len(t))
    plt.draw()
    plt.pause(0.1)
plt.show(block=True)
