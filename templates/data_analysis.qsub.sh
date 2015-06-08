#!/bin/bash
#PBS -N {{ pbs.task_name }}
#PBS -j oe
#PBS -o {{ output_dir }}/{{ pbs.task_name }}.o
#PBS -l walltime={{ pbs.walltime }}
#PBS -l nodes={{ pbs.nodes }}:ppn={{ pbs.ppn }}
#PBS -l mem={{ pbs.mem }}
#PBS -m abe
#PBS -M jbradt@msu.edu

export PYTHONPATH=$HOME/Documents/Code/pytpc:$HOME/Documents/Code/alphas-dec14:$PYTHONPATH

cd {{ output_dir }}

echo "Launching job"
{{ executable }} {{ infile }} {{ outfile }}

if [ $PBS_JOBID ]; then
  echo "Job statistics"
  qstat -f $PBS_JOBID
fi
