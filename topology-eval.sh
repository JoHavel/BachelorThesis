#!/bin/bash
#SBATCH -J symSynTopologyEval
#SBATCH --array=0-7
#SBATCH --output=tf-logs/slurm/topology-eval-%A_%a.out
#SBATCH --error=tf-logs/slurm/topology-eval-%A_%a.err
#SBATCH -p gpu-ms
#SBATCH --gpus=1
#SBATCH --mem=12gb
#SBATCH --exclude=dll-3gpu[1-5],dll-4gpu[1-4],dll-8gpu[1-6],dll-10gpu1

# I want to run only on: dll-10gpu[2,3]
# But --nodelist wants me to run on all, I want to run on some.
# So I invert it, exluding all those that aren't 'GeForce GTX 1080 Ti'

# This script trains models for the TOPOLOGY experiment
# (testing what topology should be used for synthesis)

# you do:
# sbatch ./topology-eval.sh 30

ID_TO_NAME="
A
B
C
D
E
F
G
H
"

NAME=$(echo "$ID_TO_NAME" | head -n $(expr 2 + $SLURM_ARRAY_TASK_ID) | tail -n 1)
SEED=$1

if [ -z "$SEED" ]; then
    echo "Seed argument missing"
    exit 1
fi

echo "################################"
echo "# Topology eval ${NAME}_${SEED}"
echo "################################"
echo

export LD_LIBRARY_PATH=/opt/cuda/9.0/lib64:/opt/cuda/9.0/cudnn/7.0/lib64

.venv/bin/python3 experiment_symbols.py evaluate \
    --model experiment_${NAME}_${SEED} \
    > tf-logs/stdout-eval/${NAME}_${SEED}-muscima.txt

.venv/bin/python3 experiment_symbols.py evaluate_on_real \
    --model experiment_${NAME}_${SEED} \
    > tf-logs/stdout-eval/${NAME}_${SEED}-cavatina.txt

.venv/bin/python3 experiment_symbols.py evaluate_on_primus \
    --model experiment_${NAME}_${SEED} \
    > tf-logs/stdout-eval/${NAME}_${SEED}-primus.txt

echo
echo "########"
echo "# DONE #"
echo "########"