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
    while IFS=, read -r delta theta Re We C xL yL T
    do
    
        fileout="$HOME/colab-ruben-benney/pbs-scripts/run-d-$delta-theta-$theta-Re-$Re-We-$We-C-$C-xL-$xL-yL-$yL-T-$T.pbs"
        echo "#!/bin/sh
#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=8:mem=8gb

echo Loading matlab
module load matlab

echo Copying directory
cp \$HOME/colab-ruben-benney/code \$TMPDIR -r

echo Moving into directory
cd code

echo Running matlab command
matlab -nodesktop -nojvm -r 'create($delta,$theta,$Re,$We,$C,$xL,$yL,$T); quit'

echo Moving data
mv data-* \$HOME/colab-ruben-benney/data/

echo Complete
        " > $fileout
        
        if [ $run = true ]
        then
            qsub $fileout
        fi
    done < $file
done
exit 0
