#!/bin/bash
#SBATCH -J symbolSynthesisTopology
#SBATCH --array=0-23
#SBATCH --output=tf-logs/topology-train-%A_%a.out
#SBATCH --error=tf-logs/topology-train-%A_%a.err
#SBATCH -p gpu-ms
#SBATCH --gpus=1
#SBATCH --mem=8gb
#SBATCH --mem=8gb
#SBATCH --exclude=dll-3gpu[1-5],dll-4gpu[1-4],dll-8gpu[1-6],dll-10gpu1

# I want to run only on: dll-10gpu[2,3]
# But --nodelist wants me to run on all, I want to run on some.
# So I invert it, exluding all those that aren't 'GeForce GTX 1080 Ti'

# This script trains models for the TOPOLOGY experiment
# (testing what topology should be used for synthesis)

ID_TO_NAME="
A_72
B_72
C_72
D_72
E_72
F_72
G_72
H_72
A_73
B_73
C_73
D_73
E_73
F_73
G_73
H_73
A_74
B_74
C_74
D_74
E_74
F_74
G_74
H_74
"

ID=$SLURM_ARRAY_TASK_ID
NAME=$(echo "$ID_TO_NAME" | head -n $(expr 2 + $ID) | tail -n 1)

echo "################################"
echo "# Topology train $ID = $NAME"
echo "################################"
echo

export LD_LIBRARY_PATH=/opt/cuda/9.0/lib64:/opt/cuda/9.0/cudnn/7.0/lib64

.venv/bin/python3 experiment_topology.py train \
    --model experiment_$NAME \
    --symbols datasets/topology/out/for_mashcima/$NAME \
    --seed_offset $ID

echo
echo "########"
echo "# DONE #"
echo "########"
