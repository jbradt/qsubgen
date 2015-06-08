#!/bin/bash
#PBS -N {{ pbs.task_name }}
#PBS -j oe
#PBS -l walltime={{ pbs.walltime }}
#PBS -l nodes={{ pbs.nodes }}:ppn={{ pbs.ppn }}
#PBS -l mem={{ pbs.mem }}
#PBS -m abe
#PBS -M jbradt@msu.edu

echo "Making directory for output"
OUTDIR="$HOME/jobs/sa/{{ pbs.task_name }}"
mkdir $OUTDIR
cd $OUTDIR

echo "Launching job"
{{ executable }} {{ infile }} {{ outfile }}

echo "Job statistics"
qstat -f $PBS_JOBID
