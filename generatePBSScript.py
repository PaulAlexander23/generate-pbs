#!/usr/bin/python3

import argparse
import subprocess
import os

def main():
    args = parseArguments()

    for currentFile in args.files:
        fullFilename = os.getcwd() + "/" + currentFile
        arrayJobSize = sum(1 for line in open(fullFilename))
        pbsFilename = fullFilename.replace('.csv', '.pbs')

        createPBSFile(args.walltime, args.ncpus, args.memory, arrayJobSize, 
                fullFilename, pbsFilename, args.repositoryFolder)

        if args.runPBSScript:
            runScript(pbsFilename)


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    parser.add_argument("-t","--walltime", type=str, default="24:00:00")
    parser.add_argument("-c","--ncpus", type=int, default=16)
    parser.add_argument("-m","--memory", type=int, default=8)
    parser.add_argument("-r","--runPBSScript", action="store_true")
    parser.add_argument("-f","--repositoryFolder", type=str,
            default=os.getcwd().split('/')[-2])

    return parser.parse_args()


def createPBSFile(walltime, ncpus, memory, arrayJobSize, paramsFile, pbsFilename, repoFilename):
    string = "#!/bin/sh\n\n"
    string += getPBSString(walltime, ncpus, memory, arrayJobSize)
    string += getParamsString(paramsFile, arrayJobSize)
    string += getDestString(paramsFile, arrayJobSize)
    string += getDirectoryCopyString(repoFilename)
    string += getICCopyString(paramsFile, repoFilename)
    string += getMatlabString(ncpus, walltime)
    string += getDataCopyString()

    writeToFile(pbsFilename, string)


def getPBSString(walltime, ncpus, memory, arrayJobSize):
    string = "#PBS -l walltime={}\n".format(walltime)
    string += "#PBS -l select=1:ncpus={}:mem={}gb\n".format(ncpus, memory)
    if arrayJobSize > 1:
        string += "#PBS -J 1-{}\n".format(arrayJobSize)
    string += "\n"
    return string


def getParamsString(paramsFile, arrayJobSize):
    string = "echo Getting job id\n"
    string += "MYJOBID=$(echo ${PBS_JOBID}| sed 's/.pbs//'| sed 's/\[[0-9]*\]//')\n"
    string += "echo MYJOBID: $MYJOBID\n"
    string += "\n"

    string += "echo Setting params\n"
    if arrayJobSize == 1:
        string += "params=$(sed -n 1p {})\n".format(paramsFile)
    else:
        string += "params=$(sed -n ${{PBS_ARRAY_INDEX}}p {})\n".format(paramsFile)
    string += "echo params: $params\n"
    string += "\n"
    return string

def getDestString(paramsFile, arrayJobSize):
    string = "echo Setting destination directory\n"
    folder = os.path.dirname(paramsFile)
    string += "echo folder: {}\n".format(folder)
    if arrayJobSize == 1:
        string += "destDir={}/$MYJOBID\n".format(folder)
        string += "mkdir -p $destDir\n"
    else:
        string += "destDir={}/$MYJOBID/${{PBS_ARRAY_INDEX}}\n".format(folder)
        string += "mkdir -p {}/$MYJOBID\n".format(folder)
        string += "mkdir -p $destDir\n"
    string += "echo destDir: $destDir\n"
    string += "\n"
    return string


def getDirectoryCopyString(repoFilename):
    string = "echo Copying and moving into code repository\n"
    string += "cp $HOME/Repositories/{} $TMPDIR -r\n".format(repoFilename)
    string += "echo repoFilename: {}\n".format(repoFilename)
    string += "cd $TMPDIR/{}\n".format(repoFilename)
    string += "\n"
    return string


def getICCopyString(paramsFile, repoFilename):
    string = "echo Copying ics to folder\n"
    folder = os.path.dirname(paramsFile)
    string += "cp {}/ic-* $TMPDIR/{} \n".format(folder, repoFilename)
    string += "\n"
    return string


def getMatlabString(ncpus, walltime):
    string = "echo Loading matlab\n"
    string += "module load matlab\n"
    string += "echo Running matlab command: matlab -nodesktop -nojvm -r 'maxNumCompThreads({}); main('$params', \"{}\"); quit'\n".format(ncpus, walltime)
    string += "matlab -nodesktop -nojvm -r 'maxNumCompThreads({}); main('$params', \"{}\"); quit'\n".format(ncpus, walltime)
    string += "\n"
    return string


def getDataCopyString():
    string = "echo Moving Data\n"
    string += "mv data-* $destDir\n"
    return string


def writeToFile(filename, string):
    f  = open(filename,"w+")
    f.write(string)


def runScript(pbsFilename):
    process = subprocess.Popen("qsub {}".format(pbsFilename).split(),
            stdout=subprocess.PIPE)
    output, error = process.communicate()

if __name__=="__main__":
    main()

