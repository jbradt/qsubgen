#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import glob
import re
import os
import subprocess

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('data_analysis.qsub.sh')

script_path = os.path.expanduser('~/Documents/Code/alphas-dec14/SimpleAnalysis_data_batch.py')

input_files = glob.glob(os.path.expanduser('~/Documents/Data/Alphas-Dec14/*_ps.evt'))

for ifpath in input_files:

    run_num = re.search(r'run_(\d\d\d\d)', ifpath).group(1)
    task_name = 'sa_run_' + run_num
    output_dir = os.path.join(os.path.expanduser('~/jobs/sa'), task_name)

    pbs = {'task_name': task_name, 
           'walltime': '00:30:00',
           'nodes': 1,
           'ppn': 1,
           'mem': '8gb'}

    if not (115 <= int(run_num) <= 135):
        continue

    ofpath = 'sa_raw_run_' + run_num + '.p'
    qsubpath = os.path.join(output_dir, task_name + '.qsub.sh')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(qsubpath, 'w') as f:
        template.stream(pbs=pbs, executable=script_path, output_dir=output_dir,
                        infile=ifpath, outfile=ofpath).dump(f)

    subprocess.call(['qsub', qsubpath])
