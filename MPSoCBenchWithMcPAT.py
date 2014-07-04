#!/usr/bin/env python
# -*- coding: latin1 -*-

import os, sys, re, math
import json
from subprocess import Popen, PIPE

cmdline = sys.argv[1:]

if len(cmdline) > 1:
    print "Too much args. Exiting..."
    sys.exit(1)

if len(cmdline) == 0:
	print "Usage MPSoCBenchWithMcPAT <input-file>.json"
	sys.exit(1)

if not os.path.isfile(cmdline[0]):
    print "File does not exists. Exiting..."
    sys.exit(1)

#Abre o arquivo e pega todas as informações e Executa o MPSoCBench e guarda a saida em um arquivo

jsonFile = open(cmdline[0], 'r')

MPSoCBencharguments = json.load(jsonFile)

jsonFile.close()

# Aqui eu crio o arquivo da cache
if MPSoCBencharguments['cache']['blocking'] == 'true':
	blocking = 'ac_tlm2_port'
else:
	blocking = 'ac_tlm2_nb_port'

cache_replace = [('_PROCESSOR_', MPSoCBencharguments['processor']), ('_ASSOCIATIVE_', '"'+MPSoCBencharguments['cache']['associativity']+'"'), ('_NBLOCKS_', MPSoCBencharguments['cache']['n_blocks']), ('_SBLOCK_', MPSoCBencharguments['cache']['block_size']), ('_WPOLICY_', '"'+MPSoCBencharguments['cache']['write_policy']+'"'), ('_SPOLICY_', '"'+MPSoCBencharguments['cache']['substition_policy']+'"'), ('_TYPE_', blocking)]

cache_file = open('mips_block_template.ac')

cache_data = cache_file.read();

cache_file.close()

for search, replace in cache_replace:
	cache_data = cache_data.replace(search, replace)

if MPSoCBencharguments['cache']['blocking'] == 'true':
	cache_file = open('processors/'+MPSoCBencharguments['processor']+'/'+MPSoCBencharguments['processor']+'_block.ac', 'w')
else:
	cache_file = open('processors/'+MPSoCBencharguments['processor']+'/'+MPSoCBencharguments['processor']+'_nonblock.ac', 'w')

cache_file.write(cache_data)

cache_file.close()

cache_size = (int)(MPSoCBencharguments['cache']['block_size'])*(int)(MPSoCBencharguments['cache']['n_blocks'])*32*(int)(MPSoCBencharguments['cache']['associativity'][0])

if MPSoCBencharguments['cache']['write_policy'] == 'wt':
	cache_params = (str)((str)(cache_size)+","+(str)(MPSoCBencharguments['cache']['block_size'])+","+(str)(MPSoCBencharguments['cache']['associativity'][0])+",1,10,10,32,0")
else:
	cache_params = (str)((str)(cache_size)+","+(str)(MPSoCBencharguments['cache']['block_size'])+","+(str)(MPSoCBencharguments['cache']['associativity'][0])+",1,10,10,32,1")

print cache_params

os.system("sudo ./MPSoCBench -l")
os.system("sudo ./MPSoCBench -d")

p = Popen(['sudo','./MPSoCBench', '-r', '-n='+MPSoCBencharguments['n_cores'], '-p='+MPSoCBencharguments['processor'], '-s='+MPSoCBencharguments['software'], '-i='+MPSoCBencharguments['device']], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stderr.read()
output += "\n" + p.stdout.read()

# Aqui cria-se o arquivo de entrada do McPAT
mcpat_file = open("Mips.xml")

mcpat_data = mcpat_file.read()

mcpat_replace = [('_N_CORES_', MPSoCBencharguments['n_cores']), ('_CORE_TECH_', MPSoCBencharguments['McPAT']['core_tech_node']), ('_CLOCK_RATE_', MPSoCBencharguments['McPAT']['clock_rate']),
('_PIPELINE_PER_CORE_INT', MPSoCBencharguments['McPAT']['int_pipeline_per_core']), ('_PIPELINE_PER_CORE_FLOAT', MPSoCBencharguments['McPAT']['float_pipeline_per_core']),
('_NUMBER_STAGE_INT', MPSoCBencharguments['McPAT']['number_stages_int_pipeline']), ('_NUMBER_STAGE_FLOAT', MPSoCBencharguments['McPAT']['number_stages_float_pipeline']),
('_ALU_PER_CORE_', MPSoCBencharguments['McPAT']['alu_per_core']),('_MUL_PER_CORE_', MPSoCBencharguments['McPAT']['mul_per_core']),('_FPU_PER_CORE_', MPSoCBencharguments['McPAT']['fpu_per_core'])]

for search, replace in mcpat_replace:
	mcpat_data = mcpat_data.replace(search, replace)

mpsochbench_file = open((str)(MPSoCBencharguments['output_directory'])+"mpsoc_output.out", "w")
mpsochbench_file.write(output)
mpsochbench_file.close()

del output


#Extrai informações do output do MPSoCBench
#Info: Total de instruções por core
#Info: Total de acesso às caches - miss e hit
#Info: Quantidade de instruções por segundo executadas por cada core
#Info: Tempo de cada core para realizar a tarefa
#Info: Tempo total da execução
#Total Time Taken (seconds):     90.231961
#Simulation advance (seconds):   0.003187
#MPSoCBench: Ending the time simulation measurement.
#cache: IC
#Cache statistics:
#Read:   miss: 629 (29.1069%) hit: 1532 (70.8931%)
#Write:  miss: 0 (0%) hit: 0 (0%)
#Number of block evictions: 501
#ArchC: Simulation statistics
#    Times: 26.11 user, 33.07 system, 90.24 real
#    Number of instructions executed: 1592449
#    Simulation speed: 60.99 K instr/s
mpsochbench_file = open((str)(MPSoCBencharguments['output_directory'])+"mpsoc_output.out")

numberOfInstructions = []
simulationSpeed = []
cache = []
time_total = 0
time_per_core = []
while 1:
	line = mpsochbench_file.readline()
	if not line:
		break
	pattern = "Number of instructions executed:\s(\d+)"
	prog = re.compile(pattern)
	match = prog.findall(line)
	if match:
		numberOfInstructions.append((int)(match[0]))
	pattern = "Simulation speed:\s(\d+\.\d+)\sK\sinstr/s"
	prog = re.compile(pattern)
	match = prog.findall(line)
	if match:
		simulationSpeed.append((float)(match[0]))
	pattern = "Read:\s\s\smiss:\s(\d+)\s\((\d+\.\d+)%\)\shit:\s(\d+)\s\((\d+\.\d+)%\)"
	prog = re.compile(pattern)
	match = prog.findall(line)
	if match:
		cache.append(match[0])
	pattern = "Times: (\d+\.\d+) user, (\d+\.\d+) system, (\d+\.\d+) real"
	prog = re.compile(pattern)
	match = prog.findall(line)
	if match:
		time_per_core.append(match[0])


mpsochbench_file.seek(0,0)
# here get the all instructions
data = mpsochbench_file.read()
types = MPSoCBencharguments['isa'];
accumulator = {'Int': 0, 'Branch': 0, 'Store': 0, 'Load': 0, 'Float': 0}
for typeone in types:
	for instruction in types[typeone]:
		pattern = instruction+"\s=>\s(\d+)"
		prog = re.compile(pattern)
		match = prog.findall(data)
		if match:
			accumulator[typeone] += (int)(match[0])

print accumulator

mpsochbench_file.close()
#while 1:
#	line = mpsochbench_file.readline()
#	if not line:
#		break
#	for typeone in types:
#		for instruction in types[typeone]:
#			if line.find(" "+instruction+" ") != -1:
#				accumulator[typeone] += 1;
cache_access = 0;
cache_misses = 0;
for cvalue in cache:
	cache_access += (float)(cvalue[0])+(float)(cvalue[2])
	cache_misses += (float)(cvalue[0])



mcpat_replace = [
					("_TOTAL_CYCLES_", (str)(accumulator['Int']+accumulator['Branch'])),
					("_RENAME_READS_", (str)((accumulator['Int']+accumulator['Branch'])*2)),
					("_INT_INSTRUCTION_", (str)(accumulator['Int'])),
					("_FP_INSTRUCTION_", (str)(accumulator['Float'])),
					("_BRANCH_INSTRUCTION_", (str)(accumulator['Branch'])),
					("_LOAD_INSTRUCTION_", (str)(accumulator['Load'])),
					("_STORE_INSTRUCTION_", (str)(accumulator['Store'])),
					("_FP_READS_", (str)(accumulator['Float']*2)),
					("_TOTAL_CACHE_ACCESS_", (str)(cache_access)),
					("_TOTAL_CACHE_MISSES_", (str)(cache_misses)),
					("_NOC_NODES_", (str)(math.ceil(math.sqrt((float)(MPSoCBencharguments['n_cores']))))),
					("_LOAD_PLUS_STORE_", (str)(accumulator['Load']+accumulator['Store'])),
					("_CACHE_BLOCK_SIZE_", (str)(MPSoCBencharguments['cache']['block_size'])),
					("_CACHE_SIZE_", (str)(cache_params)),
				]

for search, replace in mcpat_replace:
	mcpat_data = mcpat_data.replace(search, replace)

mcpat_file.close()

mcpat_file = open(MPSoCBencharguments['McPAT']['bin_directory']+"running_input.xml", "w")
mcpat_file.write(mcpat_data)
mcpat_file.close()

os.system("sudo "+(str)(MPSoCBencharguments['McPAT']['bin_directory'])+"./mcpat -infile "+(str)(MPSoCBencharguments['McPAT']['bin_directory'])+"running_input.xml -print_level 5 > "+(str)(MPSoCBencharguments['output_directory'])+"mcpat_out.out")

os.remove((str)(MPSoCBencharguments['output_directory'])+"mpsoc_output.out")

mpsoc_output = []
for i in range((int)(MPSoCBencharguments['n_cores'])):
	mpsoc_output.append("Core "+(str)(i))
	mpsoc_output.append("Cache statistics:")
	mpsoc_output.append("Read:   miss: "+(str)(cache[i][0])+" ("+(str)(cache[i][1])+"%) hit: "+(str)(cache[i][2])+" ("+(str)(cache[i][3])+"%)")
	mpsoc_output.append("Write:  miss: 0 (0%) hit: 0 (0%)")
	mpsoc_output.append("ArchC: Simulation statistics")
	mpsoc_output.append("    Times: "+(str)(time_per_core[i][0])+" user, "+(str)(time_per_core[i][1])+" system, "+(str)(time_per_core[i][2])+" real")
	mpsoc_output.append("    Number of instructions executed: "+(str)(numberOfInstructions[i])+"")
	mpsoc_output.append("    Simulation speed: "+(str)(simulationSpeed[i])+" K instr/s")


mpsochbench_file = open((str)(MPSoCBencharguments['output_directory'])+"mpsoc_output.out", 'w')
for i in range(len(mpsoc_output)):
	mpsochbench_file.write((str)(mpsoc_output[i])+'\n')
mpsochbench_file.close()