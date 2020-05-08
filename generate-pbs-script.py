#usr/local/bin/python3

import argparse
import subprocess
import os

def main(walltime, ncpus, memory, arrayJobSize, paramsFile, wibl1, pbsFilename, repoFilename):
    string = "#!/bin/sh\n\n"
    string += getPBSString(walltime, ncpus, memory, arrayJobSize)
    string += getParamsString(paramsFile, arrayJobSize)
    string += getDestString(paramsFile)
    string += getDirectoryCopyString(repoFilename)
    string += getICCopyString(paramsFile, repoFilename)
    string += getMatlabString(ncpus, walltime)
    string += getDataCopyString()

    print(pbsFilename)
    writeToFile(pbsFilename, string)


def writeToFile(filename, string):
    f  = open(filename,"w+")
    f.write(string)


def getPBSString(walltime, ncpus, memory, arrayJobSize):
    string = "#PBS -l walltime={}\n".format(walltime)
    string += "#PBS -l select=1:ncpus={}:mem={}gb\n".format(ncpus, memory)
    if arrayJobSize > 1:
        string += "#PBS -J 1-{}\n".format(arrayJobSize)
    string += "\n"
    return string


def getParamsString(paramsFile, arrayJobSize):
    if arrayJobSize == 1:
        string = "MYJOBID=$(echo ${PBS_JOBID}| sed 's/.pbs//')\n"
        string += "params=$(sed -n 1p {})\n".format(paramsFile)
    else:
        string = "MYJOBID=$(echo ${PBS_ARRAY_INDEX}| sed 's/\[.*//')\n"
        string += "params=$(sed -n ${{PBS_ARRAY_INDEX}}p {})\n".format(paramsFile)
    string += "\n"
    return string


def getDestString(paramsFile):
    folder = os.path.dirname(paramsFile)
    string = "destDir={}/$MYJOBID\n".format(folder)
    string += "mkdir -p $destDir\n"
    string += "\n"
    return string


def getDirectoryCopyString(repoFilename):
    string = "cp $HOME/Repositories/{} $TMPDIR -r\n".format(repoFilename)
    string += "cd $TMPDIR/{}\n".format(repoFilename)
    string += "\n"
    return string


def getICCopyString(paramsFile, repoFilename):
    folder = os.path.dirname(paramsFile)
    string = "cp {}/ic-* $TMPDIR/{} \n".format(folder, repoFilename)
    string += "\n"
    return string


def getMatlabString(ncpus, walltime):
    string = "module load matlab\n"
    string += "matlab -nodesktop -nojvm -r 'maxNumCompThreads({}); main('$params', \"{}\"); quit'\n".format(ncpus, walltime)
    string += "\n"
    return string


def getDataCopyString():
    string = "mv data-* $destDir\n"
    return string


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    parser.add_argument("-t","--walltime", type=str, default="24:00:00")
    parser.add_argument("-c","--ncpus", type=int, default=16)
    parser.add_argument("-m","--memory", type=int, default=8)
    parser.add_argument("--wibl1", action="store_true")
    parser.add_argument("-r","--runPBSScript", action="store_true")
    parser.add_argument("-f","--repositoryFolder", type=str, default=os.getcwd().split('/')[-2])

    args = parser.parse_args()

    for currentFile in args.files:
        currentFile = os.getcwd() + "/" + currentFile
        arrayJobSize = sum(1 for line in open(currentFile))
        pbsFilename = currentFile.replace('.csv', '.pbs')

        main(args.walltime, args.ncpus, args.memory, arrayJobSize, currentFile, args.wibl1, pbsFilename, args.repositoryFolder)

        if args.runPBSScript:
            process = subprocess.Popen("qsub {}".format(pbsFilename).split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
