#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import glob
import re
import os
import subprocess

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('data_analysis.qsub.sh')

script_path = '$HOME/Documents/Code/alphas-dec14/SimpleAnalysis_data_batch.py'

input_files = glob.glob(os.path.expanduser('~/Documents/Data/Alphas-Dec14/*_ps.evt'))

for ifpath in input_files[0:1]:

    run_num = re.search(r'run_(\d\d\d\d)', ifpath).group(1)
    ofpath = 'sa_raw_run_' + run_num + '.p'
    qsubpath = '$HOME/jobs/sa/sa_run_' + run_num + '.qsub.sh'

    pbs = {'task_name': 'sa_run_' + run_num,
           'walltime': '00:30:00',
           'nodes': 1,
           'ppn': 1,
           'mem': '8gb'}

    with open(qsubpath, 'w') as f:
        template.stream(pbs=pbs, executable=script_path, 
                        infile=ifpath, outfile=ofpath).dump(f)

    subprocess.call(['echo', 'qsub', qsubpath])