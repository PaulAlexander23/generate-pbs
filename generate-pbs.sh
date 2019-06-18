#!/bin/bash

run=false

while getopts hr option
do
case "${option}"
in
h) echo "$(basename -- "$0") [OPTION]... [FILE]...

Script to generate the pbs files to run the code on inputted csv file.

 Options:
  -h, Display this help and exit
  -r, Run generated scripts"
exit;;
r) run=true;;
esac
done

for file in "$@"
do
    N=$(sed -n '$=' $file)

    base=${file##*/}
    fileout="./${base%.*}.pbs"
    echo "#!/bin/sh
#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=8:mem=8gb
#PBS -J 1-$N

cp \$HOME/colab-ruben-benney/code \$TMPDIR -r
cd code

params=\$(sed -n "\${PBS_ARRAY_INDEX}p" \$HOME/colab-ruben-benney/pbs-scripts/$file)

module load matlab
matlab -nodesktop -nojvm -r 'create('\$params'); quit'

cp data-* \$HOME/colab-ruben-benney/data/
" > $fileout
        
    if [ $run = true ]
    then
        qsub $fileout
    fi
done
exit 0