#usr/local/bin/python3

import subprocess

def test_shellScript():
    bashCommand = "./generate-pbs.sh test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    actual = f.read()
    f  = open("testExpected.pbs","r")
    expected = f.read()
    assert actual == expected


def test_pythonScript():
    bashCommand = "python3 generate-pbs.py test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    actual = f.read()
    f  = open("testExpected.pbs","r")
    expected = f.read()
    assert actual == expected


def test_memoryArgument():
    bashCommand = "python3 generate-pbs.py -m 32 test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    actual = f.read()
    f  = open("testExpectedMemory.pbs","r")
    expected = f.read()
    assert actual == expected


def test_wiblArgument():
    bashCommand = "python3 generate-pbs.py --wibl1 test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    actual = f.read()
    f  = open("testExpectedWIBL1.pbs","r")
    expected = f.read()
    assert actual == expected


def test_walltimeArgument():
    bashCommand = "python3 generate-pbs.py -t 71:30:00 test.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    f  = open("test.pbs","r")
    actual = f.read()
    f  = open("testExpectedWalltime.pbs","r")
    expected = f.read()
    assert actual == expected
