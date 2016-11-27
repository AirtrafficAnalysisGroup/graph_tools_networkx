#!/bin/bash
#PBS -N air_build_graph
#PBS -l select=1:ncpus=4:mem=16gb,walltime=72:00:00
#PBS -o /home/rshaydu/airtraffic/pbsoutput/air_build_graph_err.txt
#PBS -e /home/rshaydu/airtraffic/pbsoutput/air_build_graph_out.txt

module add python
pip3 install networkx --user

cd /home/rshaydu/airtraffic

for i in {1994..2014}
do
	python3 graphbuilder.py $i 
done
