#!/usr/bin/env python
# -*- coding: latin1 -*-

import os, sys, re, math
import getopt
import json
from subprocess import Popen, PIPE
mcpat = open('m.out', 'r')

data = mcpat.read()
data = data.split('\n')

for i in range(0, len(data)):
	pattern = "Read:\s\s\smiss:\s(\d+)\s\(((\d+\.\d+)|(\d+))%\)\shit:\s(\d+)\s\(((\d+\.\d+)|(\d+))%\)"
	prog = re.compile(pattern)
	match = prog.findall(data[i])
	if match:
		print "aqui"
		#cache.append(match[0])