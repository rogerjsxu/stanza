#!/bin/bash
#SBATCH --partition=jag-lo --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10g
#SBATCH --gres=gpu:1
#SBATCH --output=/sailhome/pengqi/logs/slurm-%j.out
#SBATCH --mail-user=pengqi@cs.stanford.edu
#SBATCH --mail-type=FAIL
#SBATCH --exclude=jagupard14

echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory = "$SLURM_SUBMIT_DIR

outputprefix=$1
if [[ "$outputprefix" == "tokenize" || "$outputprefix" == "mwt" || "$outputprefix" == "lemma" || "$outputprefix" == "pos" || "$outputprefix" == "depparse" ]]; then
    outputprefix=""
else
    shift
fi
module=$1
shift
mode=$1
shift
tb=$1
shift
root=$1
shift
args=$@

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64
export PATH=/usr/local/cuda-8.0/bin:$PATH
export CUDA_HOME=/usr/local/cuda-8.0
export PATH=/juicier/scr127/scr/pengqi/anaconda3_slurm/bin:$PATH
export LD_LIBRARY_PATH=/juicier/scr127/scr/pengqi/anaconda3_slurm/lib:$LD_LIBRARY_PATH

cd $root
echo bash scripts/${mode}_${module}.sh slurm_${outputprefix} $tb 0 $args
bash scripts/${mode}_${module}.sh slurm_${outputprefix} $tb 0 $args

#
echo "Done"