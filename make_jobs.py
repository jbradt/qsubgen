#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import glob
import re
import os
import subprocess
from math import ceil
import pytpc

############### FILL THESE IN ####################

template_name = 'example.qsub.sh'  # The template to load
input_glob = '~/Documents/Data/Raw/e15503b/run_*.h5'  # Path to the input files
time_per_evt = 0.100  # the processing time required per event, in seconds
task_name_head = 'cfit_run_'  # head for the job name. This will have the run number appended to it
output_root = '~/jobs/ar46/cfit'  # root for output files. Subfolders will be created for each run.
output_suffix = '.db'  # This string is appended to the end of task_name to make the output file name.
num_nodes = 1  # number of nodes to request
ppn = 1  # processors per node
mem = '600mb'  # memory to request

##################################################


def time_string(sec):
    m, s = divmod(ceil(sec), 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


# Load template from disk
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template(template_name)

input_files = glob.glob(os.path.abspath(os.path.expanduser(input_glob)))

for i, ifpath in enumerate(input_files):
    print(ifpath)

    run_num = re.search(r'run_(\d\d\d\d)', ifpath).group(1)

    print('({}/{}) Preparing job for run {}'.format(i, len(input_files), run_num))

    task_name = task_name_head + run_num
    output_dir = os.path.join(os.path.expanduser(output_root), task_name)

    with pytpc.hdfdata.HDFDataFile(ifpath, 'r') as hf:
        nevts = len(hf)

    walltime = nevts * time_per_evt + 60*5  # I included 5 minutes of extra time here

    pbs = {'task_name': task_name,
           'walltime': time_string(walltime),
           'nodes': num_nodes,
           'ppn': ppn,
           'mem': mem}

    ofpath = task_name + '.db'
    qsubpath = os.path.join(output_dir, task_name + '.qsub.sh')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(qsubpath, 'w') as f:
        template.stream(pbs=pbs, output_dir=output_dir, infile=ifpath, outfile=ofpath).dump(f)

    # Uncomment this last line to call qsub for each job
    # subprocess.call(['qsub', qsubpath])
