#usr/local/bin/python3

import subprocess
import re

def test_pythonScript():
    bashCommand = "python3 generate-pbs-script.py test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    actual = f.read()
    f  = open("testExpected.pbs","r")
    expected = f.read()
    assert actual == expected


def test_walltimeArgument():
    bashCommand = "python3 generate-pbs-script.py -t 12:34:56 test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    for line in f:
        if "walltime" in line:
            actual = line
    expected = "#PBS -l walltime=12:34:56\n"
    assert actual == expected


def test_ncpusArgument():
    bashCommand = "python3 generate-pbs-script.py -c 8 test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    for line in f:
        for section in line.split(":"):
            if "ncpus" in section:
                actual = section
    expected = "ncpus=8"
    assert actual == expected


def test_memoryArgument():
    bashCommand = "python3 generate-pbs-script.py -m 32 test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    for line in f:
        for section in line.split(":"):
            if "mem" in section:
                actual = section
    expected = "mem=32gb\n"
    assert actual == expected
