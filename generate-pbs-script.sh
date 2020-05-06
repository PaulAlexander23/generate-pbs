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

WALLTIME=24:00:00
NNODES=1
NCPUS=16
MEMORY=8

for file in "$@"
do
    N=$(sed -n '$=' $file)

    folder="$echo${PWD##*/}"
    fileout="$folder.pbs"

    echo $fileout

    echo " #!/bin/sh

#PBS -l walltime=$WALLTIME
#PBS -l select=$NNODES:ncpus=$NCPUS:mem=${MEMORY}gb" > $fileout

    if [[ $N -gt 1 ]]
    then
        echo "#PBS -J 1-$N" >> $fileout
    fi

    echo "
echo Loading matlab
module load matlab

echo Copying repository to temporay directory
cp \$HOME/Repositories/$folder \$TMPDIR -r

echo Moving into directory
cd \$TMPDIR/$folder" >> $fileout

    
    if [[ $N -gt 1 ]]
    then
        echo "
echo Reading csv file
MYARRAYJOBID=\$(echo \${PBS_ARRAY_ID}| sed 's/\[.*//')
params=\$(sed -n "\${PBS_ARRAY_INDEX}p" $file)" >> $fileout
    else
        echo "
echo Reading csv file
params=\$(cat $file)" >> $fileout
    fi

echo "
echo Creating data destination folder
mkdir -p \$MYARRAYJOBID

echo Running matlab command
matlab -nodesktop -nojvm -r 'maxNumCompThreads($NCPUS); main('\$params', \"$WALLTIME\"); quit'

echo Moving data to destination folder
mv data-* \$MYARRAYJOBID

echo Complete" >> $fileout

    if [ $run = true ]
    then
        qsub $fileout
    fi
done
exit 0
