#!/bin/bash
###############################################################################
## SLURM Options
#SBATCH --time=04:00:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --ntasks-per-node=1             # Number of task (cores/ppn) per node
#SBATCH --cpus-per-task=2 
#SBATCH --mem=64GB
#SBATCH --job-name=indegree_distribution  # Job name
#SBATCH --partition=eng-instruction      # Partition (queue)
#SBATCH --account=25sp-cs598gck-eng      # Batch account to use
#SBATCH --output=indegree_distribution.o%j  # Name of batch job output i

# Define the network file path
NETWORK_FILE="/projects/illinois/eng/shared/shared/CS598GCK-SP25/assig2_networks/cit_hepph_cleaned.tsv"

python run_leiden.py -i $NETWORK_FILE -r 0.005 -n 2 -o cit_heph_cpm_0.005.tsv
python run_leiden.py -i $NETWORK_FILE -r 0.05 -n 2 -o cit_heph_cpm_0.05.tsv
python run_leiden.py -i $NETWORK_FILE -r 0.2 -n 2 -o cit_heph_cpm_0.2.tsv
# python run_leiden_modularity.py -i $NETWORK_FILE -n 2 -o cit_heph_modularity.tsv
