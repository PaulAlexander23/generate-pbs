#usr/local/bin/python3

import argparse

def main(walltime, memory, arrayJobSize, paramsFile, wibl1):
    string = "#!/bin/sh\n"
    string += getPBSString(walltime, memory, arrayJobSize)
    string += getDirectoryCopyString()
    string += getParamsString(paramsFile)
    string += getMatlabString(wibl1)
    string += getDataCopyString()

    writeToFile("test.pbs", string)


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
    parser.add_argument("-t","--walltime", type=str)
    parser.add_argument("-m","--memory", type=int)
    parser.add_argument("--wibl1", action="store_true")

    args = parser.parse_args()

    if args.walltime is None:
        walltime = "24:00:00"
    else:
        walltime = args.walltime

    if args.memory is None:
        memory = 8
    else:
        memory = args.memory

    if args.wibl1:
        wibl1 = True
    else:
        wibl1 = False
    for currentFile in args.files:
        arrayJobSize = sum(1 for line in open(currentFile))
        main(walltime, memory, arrayJobSize, currentFile, wibl1)
