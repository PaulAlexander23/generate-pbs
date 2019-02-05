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

    
    fileout="$HOME/colab-ruben-benney/pbs-scripts/run-${file%.*}.pbs"
    echo "#!/bin/sh
#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=16:mem=16gb
#PBS -J 1-$N

echo Loading matlab
module load matlab

echo Copying directory
cp \$HOME/colab-ruben-benney/code \$TMPDIR -r

echo Moving into directory
cd code

echo Reading csv file
line=\$(sed -e 's/,/ /g' <<< \$(sed -n '\$(PBS_ARRAY_INDEX)p' \$file))
read -r delta theta Re We C xL yL T <<< \$line

echo Running matlab command
matlab -nodesktop -nojvm -r 'create(\$delta,\$theta,\$Re,\$We,\$C,\$xL,\$yL,\$T); quit'

cp data-* \$HOME/colab-ruben-benney/data/

echo Complete
    " > $fileout
        
    if [ $run = true ]
    then
        qsub $fileout
    fi
done
exit 0
