# qsubgen

This is a template script to create PBS jobs for a set of data files. It requires `jinja2` to be installed to do the actual script generation.

## Main script

The main script, `make_jobs.py`, has a few variables at the top that should be filled in based on the requirements of your particular job. Namely, you should fill in the time per job, paths to the input and output directories, memory and processors required, etc. Other parameters can also be added depending on what needs to be done.

## Templates

The qsub scripts for each job are generated based on a template in the directory `templates`. This is a [Jinja2](http://jinja.pocoo.org/docs/dev/) template, which, for our purposes, means that anything that looks like `{{ this }}` is a field that will be filled in by the code. The example script I included has only 4 fields: `{{ pbs }}` to provide the job's requirements, `{{ infile }}` to provide the path to the input file for each job, `{{ outfile }}` for the output file, and `{{ output_dir }}` for the output directory. These will be replaced by an appropriate value wherever they are used in the template.

You will need to modify the provided template to fill in the details about your job, like which command to run.

## Running the jobs

To actually run the jobs (instead of just creating the batch scripts), un-comment the last line in `make_jobs.py`. Alternatively, in the directory containing all of the batch scripts, try something like
```bash
$ ls */*.qsub.sh | xargs -L1 qsub
```
