#!/usr/bin/python
# coding:utf-8
# Create By : Jky
# Ping a url or IP

import os
import sys
import commands
import re
import time
import json
import socket

class Resource():
        def __init__(self,ip):
                self.host = socket.gethostname()
                self.ip = ip

        def run(self):
                ip = 'www.baidu.com'

                cmd ='ping -i 0.2 -c 3 -w 3 %s' % (ip) #ping 3次，超时3s
                ret = commands.getoutput(cmd)
                loss_re = re.compile(r"received, (.*) packet loss")
                packet_loss = loss_re.findall(ret)[0]
                rtt_re = re.compile(r"rtt min/avg/max/mdev = (.*) ")
                rtts = rtt_re.findall(ret)
                if rtts:
                        rtt = rtts[0].split('/')
                        rtt_min = rtt[0]
                        rtt_avg = rtt[1]
                        rtt_max = rtt[2]
                else:
                        rtt_min = 0
                        rtt_avg = 0
                        rtt_max = 0

                packet_loss = packet_loss.split('%')[0]

                ########## For Jmonitor ##########
                self.resource_d={
                        'ping.loss':[packet_loss,'GAUGE'],
                        'ping.rtt_min':[rtt_min,'GAUGE'],
                        'ping.rtt_avg':[rtt_avg,'GAUGE'],
                        'ping.rtt_max':[rtt_max,'GAUGE']
                }
                output = []
                for resource in self.resource_d.keys():
                        t = {}
                        t['endpoint'] = self.host
                        t['timestamp'] = int(time.time())
                        t['step'] = 60
                        t['counterType'] = self.resource_d[resource][1]
                        t['metric'] = resource
                        t['value']= self.resource_d[resource][0]
                        t['tags'] = 'url=%s' %self.ip

                        output.append(t)
                return output
        def dump_data(self):
                return json.dumps()

if __name__ == "__main__":
    d = Resource('www.baidu.com').run()
    if d:
        print json.dumps(d)
