Integration between MPSoCBench and McPAT 
========================================

This repository contains the Vagrantfile to instantiate a virtual machine capable of executing platforms described through a json file in both tools (MPSoCBench and McPAT).

Dependencies
============

- [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](http://www.vagrantup.com/downloads.html)
- SystemC: The SystemC license does not allow distribution of the source code. So, you need to download its last version in the oficial website, and put the file systemc-2.3.1.tgz at the same folder that the Vagrant files. After this, our Vagrant script will build and install SystemC and other tools properly.


How to Install ?
================

- First clone or download as zip this respository.
- Extract the file in some directory on your computer.
- Then download the  [systemc-2.3.1.tgz (includes TLM)](http://www.accellera.org/downloads/standards/systemc).
- Copy the systemc-2.3.1.tgz to same directory of integration.
- So open a terminal and enter the directory of integration and execute:

		$ vagrant up

- Please wait until instantiation is complete.
- So, you can now access virtual machine via ssh and go to the correct folder:

		$ vagrant ssh
		$ cd /opt/MPSoCBench

Run your first simulator with McPAT
========================

- After installing all tools, start you virtual machine and go to the Integration folder:

		$ vagrant up
		$ vagrant ssh
		$ cd /opt/MPSoCBench

- Build your first multicore platform (example: dual-core MIPS, connected by a NoC, able for running dijkstra):

		$ sudo python MPSoCBenchWithMcPAT.py /vagrant/input-example.json

- Following the specifications of the parameters of the json file.

		{
			"processor" : "mips", // (mips, sparc, powerpc)
			"n_cores" : "2", // (2, 4, 8, 16, 32, 64)
			"software" : "dijkstra", // ()
			"device" : "noc.at", // (router.lt, noc.lt, noc.at)
			"cache": {"associativity" : "8w", "n_blocks" : "64", "block_size" : "16", "write_policy" : "wb", "substition_policy" : "fifo", "blocking" : "false"},
			"McPAT" : {
				"bin_directory" : "/vagrant/mcpat/",
				"clock_rate" : "322",
				"core_tech_node" : "22",
				"int_pipeline_per_core" : "1",
				"float_pipeline_per_core" : "1",
				"number_stages_int_pipeline" : "5",
				"number_stages_float_pipeline" : "7",
				"alu_per_core" : "1",
				"mul_per_core" : "1",
				"fpu_per_core" : "1"
			},
			"output_directory" : "/vagrant/execute/", //Output directory of simulation
			"isa" : { // Here's ISA processor separately by type. Recalling that the instructions of loads and stores should be in the group of integers too.
			    "Int": [
			        "lb",
			        "lbu",
			        "lh",
			        "lhu",
			        "lw",
			        "lwl",
			        "lwr",
			        "sb",
			        "sh",
			        "sw",
			        "swl",
			        "swr",
			        "addi",
			        "addiu",
			        "slti",
			        "sltiu",
			        "andi",
			        "ori",
			        "xori",
			        "lui",
			        "add",
			        "addu",
			        "sub",
			        "subu",
			        "slt",
			        "sltu",
			        "instr_and",
			        "instr_or",
			        "instr_xor",
			        "instr_nor",
			        "nop",
			        "sll",
			        "srl",
			        "sra",
			        "sllv",
			        "srlv",
			        "srav",
			        "mult",
			        "multu",
			        "div",
			        "divu",
			        "mfhi",
			        "mthi",
			        "mflo",
			        "mtlo",
			        "sys_call",
			        "instr_break"
			    ],
			    "Branch": [
			        "j",
			        "jal",
			        "jr",
			        "jalr",
			        "beq",
			        "bne",
			        "blez",
			        "bgtz",
			        "bltz",
			        "bgez",
			        "bltzal",
			        "bgezal"
			    ],
			    "Store": [
			        "sb",
			        "sh",
			        "sw",
			        "swl",
			        "swr"
			    ],
			    "Load": [
			        "lb",
			        "lbu",
			        "lh",
			        "lhu",
			        "lw",
			        "lwl",
			        "lwr"
			    ],
			    "Float" : [
			    ]
			}
		}


- You can stop the virtual machine with:
	
		$ vagrant halt