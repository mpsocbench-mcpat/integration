#!/usr/bin/env python
# -*- coding: latin1 -*-

import os, sys, re, math
import getopt
import json
from subprocess import Popen, PIPE

cmdline = sys.argv[1:]

if len(cmdline) == 0:
	print "Usage Backtracking.py -n <2^(k),2^(k+c)> -a <mm^2> -t <22 | 32 | 45> -c <2^(k)kBytes> -m <>.json -s <>"
	sys.exit(1)

#if not os.path.isfile(cmdline[4]):
#    print "File does not exists. Exiting..."
#    sys.exit(1)




try:
	opts, args = getopt.getopt(cmdline,"hn:a:t:c:m:s:")
except getopt.GetoptError:
	print 'Usage Backtracking.py -n <2^(k),2^(k+c)> -a <mm^2> -t <22 | 32 | 45> -c <2^(k)kBytes> -m <>.json -s <>'
	sys.exit(2)

for opt, arg in opts:
	if opt == '-n':
		ranged = arg.split(',')
	if opt == '-a':
		area = arg
	if opt == '-t':
		tec = arg
	if opt == '-c':
		cache = arg
	if opt == '-s':
		softwares = arg.split(',')
	if opt == '-m':
		try:
			template = open(arg, 'r')
		except Exception, e:
			sys.exit(1)
print ranged

template_data = template.read()

core = (int)(ranged[0])

while core <= (int)(ranged[1]):

	core_replace = [['_N_CORES_', (str)(core)], ['_TECHNOLOGY_', tec]]

	for software in softwares:
		software_replace = [['_SOFTWARE_', (str)(software)]]

		cachet = (int)(cache)
		print software
		while cachet <= 512:
			if cachet in (32, 128, 512):
				block_size = 8
			else:
				block_size = 4

			if cachet == 32:
				associativity = n_blocks = 32
			elif cachet in (64, 128):
				associativity = n_blocks = 64
			elif cachet in (256, 512):
				associativity = n_blocks = 128

			tdata = template_data

			cache_replace = [['_ASSOC_', (str)(associativity)+'w'], ['_N_BLOCKS_', (str)(n_blocks)], ['_BLOCK_S_', (str)(block_size)]]
			for search, replace in cache_replace:
				tdata = tdata.replace(search, replace)
			for search, replace in software_replace:
				tdata = tdata.replace(search, replace)
			for search, replace in core_replace:
				tdata = tdata.replace(search, replace)
			for search, replace in [['_OUTPUT_', sys.path[0]+'/']]:
				tdata = tdata.replace(search, replace)
			out = open((str)(core) + '_' + (str)(software) + '_' + (str)(cachet) + '.json', 'w')
			out.write(tdata)
			out.close()

			os.system("cd /opt/MPSoCBench && sudo python MPSoCBenchWithMcPAT.py " + sys.path[0] + '/' + (str)(core) + '_' + (str)(software) + '_' + (str)(cachet) + '.json')

			os.rename('mcpat_out.out', (str)(core) + '_' + (str)(software) + '_' + (str)(cachet) + '_mcpat.out')
			os.rename('mpsoc_output.out', (str)(core) + '_' + (str)(software) + '_' + (str)(cachet) + '_mpsoc.out')

			 
  			

  			mcpat = open((str)(core) + '_' + (str)(software) + '_' + (str)(cachet) + '_mcpat.out', 'r')

  			data = mcpat.read()
  			data = data.split('\n')
  			saiu = 0
  			for i in range(0, len(data)):
	  			pattern = "Processor:"
				prog = re.compile(pattern)
				match = prog.findall(data[i])
				if match:
					pattern = "Area = (\d+\.\d+)"
					prog = re.compile(pattern)
					match = prog.findall(data[i+1])
					if (float)(match[0]) > (float)(area):
						print "O limite superior de área foi atingido com " + (str)(core) + " núcleos rodando " + (str)(software) + " e tendo " + (str)(cachet) + "kBytes de cache"
						saiu = 1
						break;
			if saiu == 1:
				break;
			mcpat.close()
			#print associativity*32*block_size*n_blocks
			
			cachet *=2

	core *= 2
print "O limite superior de área foi não atingido."
#MPSoCBencharguments['cache']['block_size'])*(int)(MPSoCBencharguments['cache']['n_blocks'])*32*(int)(MPSoCBencharguments['cache']['associativity'][0:-1]
#(32^2)*32*8 = 262144
#(64^2)*32*4 = 524288
#(64^2)*32*8 = 128
#(128^2)*32*4 = 2097152
#(128^2)*32*8 = 512
