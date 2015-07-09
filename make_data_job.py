#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import glob
import re
import os
import subprocess
from math import ceil

import sys
sys.path.append(os.path.expanduser('~/Documents/Code/pytpc/'))
import pytpc

def time_string(sec):
    m, s = divmod(ceil(sec), 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('data_analysis.qsub.sh')

script_path = os.path.expanduser('~/Documents/Code/alphas-dec14/SimpleAnalysis_data_batch.py')

input_files = glob.glob(os.path.expanduser('~/Documents/Data/Alphas-Dec14/*_ps.evt'))

time_per_evt = 0.35  # the processing time required per event

for ifpath in input_files:

    run_num = re.search(r'run_(\d\d\d\d)', ifpath).group(1)
    task_name = 'sa_run_' + run_num
    output_dir = os.path.join(os.path.expanduser('~/jobs/sa'), task_name)

    efile = pytpc.EventFile(ifpath)
    walltime = len(efile) * time_per_evt
    efile.close()
    del efile

    pbs = {'task_name': task_name, 
           'walltime': time_string(walltime),
           'nodes': 1,
           'ppn': 1,
           'mem': '500mb'}

    if not (38 <= int(run_num) <= 295):
        continue

    ofpath = 'sa_raw_run_' + run_num + '.db'
    qsubpath = os.path.join(output_dir, task_name + '.qsub.sh')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(qsubpath, 'w') as f:
        template.stream(pbs=pbs, executable=script_path, output_dir=output_dir,
                        infile=ifpath, outfile=ofpath).dump(f)

    subprocess.call(['qsub', qsubpath])
