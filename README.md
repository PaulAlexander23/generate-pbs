# Generator Scripts

Repository containing the scripts to generate the pbs files to submit to the cluster.

We need a separate repository because these scripts should be mostly project independent and it would be good to have version control for these files too.

The solution should:
 - Take in a .csv parameter file
 - Create a pbs file using the parameter file name
 - Use supplied (default) pbs variables: walltime ("24:00:00"), ncpus (16), memory (8)
 - Use a pbs array if there is more than one line in the parameter file
 - Load Matlab
 - Limit number of cores Matlab can use to ncpus
 - Copy supplied Repository if given or ~/Repositories/'parent directory'
 - Run main.m
 - Use a temporary directory for the execution of the main function
 - Submit the pbs script to cluster if -r flag is used

Usage:

    python generatePBSScript.py [-h] [-t WALLTIME] [-c NCPUS] [-m MEMORY]
                                  [-r] [-f REPOSITORYFOLDER]
                                  files [files ...]

Testing:

    pytest
