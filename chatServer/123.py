#!/usr/bin/env python
# encoding: utf-8
'''
Define some common function

Create on 03/31/2019
@author: Siqi Zeng

'''
import json
import datetime


time = datetime.datetime(2019,1,1,12,13,12)
time_new = strftime(time)
data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

json = json.dumps(data)
print json