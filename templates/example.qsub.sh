#!/bin/bash
#PBS -N {{ pbs.task_name }}
#PBS -j oe
#PBS -o {{ output_dir }}/{{ pbs.task_name }}.o
#PBS -l walltime={{ pbs.walltime }}
#PBS -l nodes={{ pbs.nodes }}:ppn={{ pbs.ppn }}
#PBS -l mem={{ pbs.mem }}

cd {{ output_dir }}

echo "Launching job"
# Fill in the command for your executable here. Use {{ infile }} and {{ outfile }} as placeholders for the
# input and output files, respectively.
/path/to/executable {{ infile }} {{ outfile }}

if [ $PBS_JOBID ]; then
  echo "Job statistics"
  qstat -f $PBS_JOBID
fi
