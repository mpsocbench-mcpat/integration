#!/bin/bash
if [ ! -f /vagrant/systemc-2.3.1.tgz ];
then
echo "File systemc-2.3.1.tgz does not exist, please download the file in http://www.accellera.org/downloads/standards/systemc"
exit
fi
sudo apt-get update
sudo apt-get -y install gcc
sudo apt-get -y install g++
sudo apt-get -y install python
sudo apt-get -y install unzip
sudo apt-get -y install make
sudo apt-get -y install gawk
sudo apt-get -y install libc6-i386
sudo apt-get -y install vim
sudo apt-get install -y m4
sudo apt-get install -y patch
sudo apt-get install -y apache2
sudo apt-get install -y php5 php5-curl
rm -Rf /var/www
ln -s /vagrant /var/www
cp /vagrant/systemc-2.3.1.tgz /home/vagrant/systemc.tgz
sudo tar -xvf systemc.tgz
sudo mv systemc-2.3.1 /opt/systemc
cd /opt/systemc
make uninstall
sudo ./configure --prefix=/opt/systemc
sudo make
sudo make install
cd /home/vagrant
sudo wget http://sourceforge.net/projects/archc/files/MPSoCBench/1.2/archc.tar.gz/download
sudo tar -xvf download
sudo mv archc /opt/archc
cd /opt/archc
sudo make uninstall #if yout want to remove old versions 
sudo ./configure --prefix=/opt/archc --with-systemc=/opt/systemc --with-tlm=/opt/systemc/include
sudo make
sudo make install
sudo mkdir /l
sudo mkdir /l/archc
cd /home/vagrant
sudo rm download
sudo wget http://sourceforge.net/projects/archc/files/MPSoCBench/1.1/compilers.tar.gz/download
sudo tar -xvf download
sudo mv compilers /l/archc/compilers
cd /home/vagrant
sudo rm download
sudo wget http://sourceforge.net/projects/archc/files/MPSoCBench/1.1/powersc.tar.gz/download
sudo tar -xvf download
sudo mv powersc /opt/powersc
cd /opt/powersc
sudo ./configure --prefix=/opt/powersc --with-systemc=/opt/systemc
sudo make
sudo make install
cd /home/vagrant
sudo rm download
sudo wget https://github.com/mpsocbench-mcpat/mpsocbench/archive/master.zip
sudo unzip master.zip
sudo mv mpsocbench-master /opt/MPSoCBench
cd /opt/MPSoCBench
sudo echo -e "export SYSTEMC:=/opt/systemc\nexport TLM_PATH := /opt/systemc/include\nexport ARCHC_PATH := /opt/archc\nexport POWERSC_PATH := /opt/powersc\nexport ARP:=\$(PWD)\nexport PATH:=/l/archc/compilers/arm/bin:/l/archc/compilers/bin:/opt/archc/bin:\$(PATH)\nexport HOST_OS:= linux\nexport LD_LIBRARY_PATH:=/opt/systemc/lib-linux:\$(LD LIBRARY PATH)" > Makefile.conf
sudo cp /vagrant/MPSoCBenchWithMcPAT.py /opt/MPSoCBench/MPSoCBenchWithMcPAT.py
sudo cp /vagrant/Mips.xml /opt/MPSoCBench/Mips.xml
sudo cp /vagrant/mips_block_template.ac /opt/MPSoCBench/mips_block_template.ac
cd /vagrant/mcpat
sudo make
sudo chmod -R 777 /opt/MPSoCBench