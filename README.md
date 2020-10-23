# Generator Scripts

Repository containing the scripts to generate the pbs files to submit to the cluster.

We need a separate repository because these scripts should be mostly project independent and it would be good to have version control for these files too.

Usage:

    python generate-pbs-script.py [-h] [-t WALLTIME] [-c NCPUS] [-m MEMORY]
                                  [-r] [-f REPOSITORYFOLDER]
                                  files [files ...]

Testing:

    pytest
