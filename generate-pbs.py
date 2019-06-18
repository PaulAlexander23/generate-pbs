#usr/local/bin/python3

import argparse
import subprocess

def main(walltime, memory, arrayJobSize, paramsFile, wibl1, pbsFilename):
    string = "#!/bin/sh\n"
    string += getPBSString(walltime, memory, arrayJobSize)
    string += getDirectoryCopyString()
    string += getParamsString(paramsFile)
    string += getMatlabString(wibl1)
    string += getDataCopyString()

    print(pbsFilename)
    writeToFile(pbsFilename, string)


def writeToFile(filename, string):
    f  = open(filename,"w+")
    f.write(string)


def getPBSString(walltime, memory, arrayJobSize):
    string = "#PBS -l walltime={}\n".format(walltime)
    string += "#PBS -l select=1:ncpus=8:mem={}gb\n".format(memory)
    string += "#PBS -J 1-{}\n".format(arrayJobSize)
    string += "\n"
    return string


def getDirectoryCopyString():
    string = "cp $HOME/colab-ruben-benney/code $TMPDIR -r\n"
    string += "cd code\n"
    string += "\n"
    return string


def getParamsString(paramsFile):
    string = "params=$(sed -n ${{PBS_ARRAY_INDEX}}p $HOME/colab-ruben-benney/pbs-scripts/{})\n".format(paramsFile)
    string += "\n"
    return string


def getMatlabString(wibl1):
    string = "module load matlab\n"
    if wibl1:
        string += "matlab -nodesktop -nojvm -r 'createWIBL1('$params'); quit'\n"
    else:
        string += "matlab -nodesktop -nojvm -r 'create('$params'); quit'\n"
    string += "\n"
    return string


def getDataCopyString():
    string = "cp data-* $HOME/colab-ruben-benney/data/\n"
    string += "\n"
    return string


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    parser.add_argument("-t","--walltime", type=str, default="24:00:00")
    parser.add_argument("-m","--memory", type=int, default=8)
    parser.add_argument("--wibl1", action="store_true")
    parser.add_argument("-r","--runPBSScript", action="store_true")
    parser.add_argument("-o","--outputDirectory", type=str, default="")

    args = parser.parse_args()

    for currentFile in args.files:
        currentFile = currentFile.split('/')[-1]
        arrayJobSize = sum(1 for line in open(currentFile))
        pbsFilename = args.outputDirectory + currentFile.rstrip('.csv') + '.pbs'
        main(args.walltime, args.memory, arrayJobSize, currentFile, args.wibl1, pbsFilename)
        if args.runPBSScript:
            process = subprocess.Popen("qsub {}".format(pbsFilename).split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
