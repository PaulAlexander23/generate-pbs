#!/usr/bin/python3

import argparse
import subprocess
from pbsStringFunctions import *

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


def writeToFile(filename, string):
    f  = open(filename,"w+")
    f.write(string)


def runScript(pbsFilename):
    process = subprocess.Popen("qsub {}".format(pbsFilename).split(),
            stdout=subprocess.PIPE)
    output, error = process.communicate()

if __name__=="__main__":
    main()
