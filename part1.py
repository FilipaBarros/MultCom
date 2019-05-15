# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:42:27 2019

@author: anafi
"""

import socket
import matplotlib.pyplot as plt
import time



def convert_to_int(date):
    total = (date.year* 31556926* 1000000) + (date.month *1000000 *2629743.83) + (date.day * 1000000 * 86400) + (date.hour * 3600 * 1000000) + (date.minute * 1000000 * 60) + (date.second*1000000) + date.microsecond
    #print(int(total))
    #print(date.microsecond)
    #print(total)
   #seconds = seconds 
    return total

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

address = "129.187.223.200"
port = 2000

#testing the socket 
packet = "TEST".ljust(1000);
packet_size = len(packet);


delays = [];    
delay = 0;
bottlenecks = [];
bottleneck = 0;
receiving_time = [];
bottlenecks_means = [];
bottleneck_sum = 0;


for j in range (1000,10000,100):
    packet = "TEST".ljust(j);
    bottleneck_sum = 0;
    for i in range (200):
        sock.sendto(packet.encode(),(address,port));
        data = sock.recv(10000);
        ts = int(time.time_ns())
        receiving_time.append(ts);
        if (i > 0):
            delay = abs(receiving_time[i] - receiving_time[i-1])
            delays.append(delay);
            if (delay == 0):
                bottleneck = 0;
            else: 
                bottleneck = packet_size/delay;   #bits/nanoseconds
            bottlenecks.append(bottleneck)
            bottleneck_sum += bottleneck
    bottlenecks_means.append(bottleneck_sum/199);

x = list(range(1000,10000,100));
y = bottlenecks_means;
plt.plot(x, y, 'b-', label='data')
plt.plot(x, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('N')
plt.grid()
plt.legend()

print('lala')  
 


#to dos      -> ajustar a fórmula para a diferença de tempo -> rever
#            -> preencher a string com white space
#            -> fazer uma função para ir mudando o tamanho dos pacotes 
#            -> fazer um ciclo de 200 para cada um dos tamanhos de pacote que calcula o delay entre dois pacotes backtoback
#            -> descobrir como é que se faz para mandar valores quando se corre o ficheiro
#            -> fazer a fórmula para o bottleneck link 
#            -> fazer os gráficos com os bottlenecks vs o tamanho dos pacotes
 

#Doubts: 
    #Mean bottleneck?
    #packets size?
    
#code for time adjustmnent: t = datetime.datetime.now()
#                           print(time.mktime(t.timetupe()))


