# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:29:31 2019

@author: anafi
"""

import socket
import matplotlib.pyplot as plt
import time
from sys import argv
import bitstring
import operator
#import md5


payload = []

def parse_packet(packet):
    bit_array = bitstring.BitArray(bytes = packet)
    version = bit_array[0:2].uint
    padding = bit_array[3]
    extension = bit_array[4]
    csrc_count = bit_array[4:8].uint
    marker = bit_array[9]
    payload_type = bit_array[9:16].uint
    sequence_number = bit_array[16:32].uint
    time_stamp = bit_array[32:64].uint
    ssrc = bit_array[64:96].uint
    #cids = []
    #temp_count = 96
    #for x in range(csrc_count):
    #    cids.append(bit_array[temp_count:temp_count+32].uint)
    #    temp_count += 32
    data = bit_array[96:]
    payload.append({"seq":sequence_number,"data":data})

def md5func(filename):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for part in iter(lambda: f.read(4096), b""):
            hash_md5.update(part)
        print(hash_md5.hexdigest())


lower_bound = 200 
upper_bound = 1500


#connect to server 
#creating the socket -> Task 1
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
address = "129.187.223.200"
port = 3000

#Retrieving the text -> Task 2
def task2():
    s = ''
    data = ""
    packet = "TEXT"
    sock.settimeout(10);
    read1 = True
    sock.sendto(packet.encode(),(address,port));
    #while True:
    #    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #    print ("received message:", data)
    file = open('TextFile.txt','w') 
    while (s != 'END\x00'):
        time_out = 0;
        try:
            #print("entrei")
            data = sock.recv(900);
            s = data.decode()
            if (s != 'END\x00'):
                file.write(s.rstrip('\0'))
        except socket.timeout:
            #print("sai")
            read1 = False
            time_out = time_out + 1;
        ts1 = int(time.time_ns());
        if(not read1):
            continue
    file.close()
    file = open('TextFile.txt','r') 
    print(file.read())
    file.close()


#read RTP traffic of an audio file -> Task 3
# MUSIC STU_ID
def task3():
    global payload
    payload=[]
    packet = "MUSIC 03714404"
    
    read1 = True
    sock.sendto(packet.encode(),(address,port));
    s = ""
    while (True):
        time_out = 0;
        try:
            #print("entrei")
            data = sock.recv(900);
            #s = data.decode()
            try:
                if( data.decode() == 'END\x00'):
                    print("Last Packet")
                    break
            except:
                parse_packet(data)
                continue
        except socket.timeout:
            #print("sai")
            read1 = False
            time_out = time_out + 1;
        ts1 = int(time.time_ns());
        if(not read1):
            continue
    
    with open("sound.mp3", "ab") as filemp3:
        print("writing")
        payload.sort(key=operator.itemgetter('seq'))
        realtotalpackets = len(payload)
        expectedpackets =  payload[len(payload)-1]["seq"] - payload[0]["seq"] + 1
        print("total/expected -> " + str(realtotalpackets) + ":" + str(expectedpackets))
        if(realtotalpackets < expectedpackets):
            print("Packets missing")
        for x in payload:
            filemp3.write(x["data"].tobytes())
        md5func("sound.mp3")
        filemp3.close()


#read RTP traffic of an audio file -> Task 4
# VIDEO STU_ID
def missing_elements(L):
    start, end = L[0], L[-1]
    return sorted(set(range(start, end + 1)).difference(L))
            

def recursivetrial():  
    numbers = []
    for v in payload:
        numbers.append(v["seq"])
    for missing in missing_elements(numbers):
        packet = "R " + str(missing)
        #print(packet)
        sock.sendto(packet.encode(),(address,port));
        try:
            #print("entrei")
            data = sock.recv(900);
            #s = data.decode()
            try:
                if( data.decode() == 'END\x00'):
                    print("Last Packet")
                    break
            except:
                parse_packet(data)
                continue
        except socket.timeout:
            #print("sai")
            continue
    payload.sort(key=operator.itemgetter('seq'))
    realtotalpackets = len(payload)
    expectedpackets =  payload[len(payload)-1]["seq"] - payload[0]["seq"] + 1
    if(realtotalpackets < expectedpackets):
        numbers = []
        recursivetrial()
    else:
        return

def task4():
    global payload
    payload=[]
    packet = "VIDEO 03714404"
    realtotalpackets = 0
    expectedpackets = 0
    read1 = True
    sock.sendto(packet.encode(),(address,port));
    s = ""
    while (True):
        time_out = 0;
        try:
            #print("entrei")
            data = sock.recv(900);
            #s = data.decode()
            try:
                if( data.decode() == 'END\x00'):
                    print("Last Packet")
                    break
            except:
                parse_packet(data)
                continue
        except socket.timeout:
            #print("sai")
            read1 = False
            time_out = time_out + 1;
        ts1 = int(time.time_ns());
        if(not read1):
            continue
    payload.sort(key=operator.itemgetter('seq'))
    realtotalpackets = len(payload)
    expectedpackets =  payload[len(payload)-1]["seq"] - payload[0]["seq"] + 1
    
    with open("video_no_retransmission.bin", "ab") as movie:
        print("writing")
    
        print("total/expected -> " + str(realtotalpackets) + ":" + str(expectedpackets))
        for x in payload:
            movie.write(x["data"].tobytes())
        movie.close()
    
    if(realtotalpackets < expectedpackets):
        recursivetrial()
        
    realtotalpackets = len(payload)
    
    with open("video_with_retransmission.bin", "ab") as movie:
        print("writing")
    
        print("total/expected -> " + str(realtotalpackets) + ":" + str(expectedpackets))
        for x in payload:
            movie.write(x["data"].tobytes())
        movie.close()
            
task2()
task3()
task4()















