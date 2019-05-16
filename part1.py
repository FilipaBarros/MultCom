# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:42:27 2019

@author: anafi
"""

import socket
import matplotlib.pyplot as plt
import time


#creating the socket -> Task 1
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
address = "129.187.223.200"
port = 2000

#testing the socket -> Task 2
packet = "TEST".ljust(400);
sock.sendto(packet.encode(),(address,port));
data = sock.recv(400);
print('message received:', data);

#sending two back to back packets and recording the time -> task 3.a, 3.b and 3.c
packet = "a".ljust(1000);
sock.sendto(packet.encode(),(address,port));
sock.sendto(packet.encode(),(address,port));
data = sock.recv(1000);
ts1 = int(time.time_ns());
data = sock.recv(1000);
ts2 = int(time.time_ns());
delay= abs(ts2 - ts1);
print('The delay for the two small back to back packets is ',  delay, 'nanoseconds');
if (delay == 0):
    bottleneck = 0;
else:
    bottleneck = len(packet)/delay;
print('The bottleneck is ',  bottleneck);



#task 3.d abd 3.e -> repeating the measure for 200 times for each packet size


r1 = 200;
r2 = 1500;
pace = int((r2 - r1)/5)

bottlenecks = [[],[],[],[],[],[]];
bottlenecks_means = [];
delays = []
sock.settimeout(2);
n = 0;
for j in range (r1,r2+1,pace):
    packet = "a".ljust(j);
    packet_size = len(packet);
    bottleneck_sum = 0;
    delay_0 = 0;
    i = 0;
    while i <= 200:
        print(i);
        sock.sendto(packet.encode(),(address,port));
        sock.sendto(packet.encode(),(address,port));
        data = None;
        read1 = True
        read2 = True
        try:
            data = sock.recv(j);
        except socket.timeout:
            read1 = False
        ts1 = int(time.time_ns());
        try:
            data = sock.recv(j);
        except socket.timeout:
            read2 = False
        ts2 = int(time.time_ns());
        
        if(i >= 0 and (not read1 or not read2)):
            continue

        delay= abs(ts2 - ts1);
        if (delay == 0):
            i = i - 1;
            delay_0 = delay_0 + 1;
     
        else: 
            bottleneck = packet_size/delay;
            bottlenecks[n].append(bottleneck);
            bottleneck_sum = bottleneck_sum + bottleneck;
        i = i + 1;
    bottlenecks_means.append(bottleneck_sum/201);
    delays.append(delay);
    n = n + 1;
    #print(n);
    #print(j);
    

#plot the bottlenecks for each packet size
x = list(range(0,201))
fig = plt.figure(figsize=(12,30));
#p = [];
for i in range(len(bottlenecks)):
    #print (len(bottlenecks[i]));
    p = r1 + i*pace;    
    l = 'bottlenecks from size packet ' + str(p);
    y = bottlenecks[i];
    ax = fig.add_subplot(6, 1, i + 1)
    ax.plot(x,y, 'o', linewidth=2, markersize=2, label=l);
    ax.set_ylabel('Bottleneck')
    ax.set_xlabel('N')
    ax.legend()
    #print (i);
        
#plot the bottleneck mean for each packet size
x = list(range(r1,r2+1,pace));
y = bottlenecks_means;
fig = plt.figure(figsize = (10,10));
ax = fig.add_subplot(1, 1, 1)
l = "Mean Bottleneck link per packet size"
ax.plot(x,y, linewidth=4, markersize=6, label=l);
ax.set_ylabel('Mean bottleneck')
ax.set_xlabel('Packet Size')
ax.legend()
 
    


