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

Run your first simulator
========================

- After installing all tools, start you virtual machine and go to the Integration folder:
		$ vagrant up
		$ vagrant ssh
		$ cd /opt/MPSoCBench
- Build your first multicore platform (example: quad-core MIPS with power estimation, connected by a router, able for running dijkstra):

		$ ./MPSoCBench -p=mips -pw -s=dijkstra -i=router.lt -n=4 -b
- Simulate your first multicore platform:

		$ ./MPSoCBench -p=mips -pw -s=dijkstra -i=router.lt -n=4 -r
- Go to [How To Use](http://archc.sourceforge.net/benchs/mpsocbench/howtouse.html) to see other examples of this benchmark.

- You can stop the virtual machine with:
	
		$ vagrant halt