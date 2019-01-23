#######################################################
#    Author:      Jacob Laster
#    email:       jlaster
#    ID:          ee364e08
#    Date:        1/23/19
#######################################################

import os
from os import *
import sys

# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################
DataPath = path.expanduser('~ee364/DataFolder/Prelab03')

#circuits and maps
def listDir():
    return [f for f in os.listdir(DataPath) if os.path.isfile(os.path.join(DataPath, f))]

def circuitDict():
    cdict = {}
    with open(path.join(DataPath, 'maps/projects.dat'), "r") as file:
        projects = [f.strip().split() for f in file.readlines()[2:]]
    for p in projects:
        if p[1] in cdict:
            cdict[p[1]].append(p[0])
        else:
            cdict[p[1]] = [p[0]]
    return cdict

def projectDict():
    pdict = {}
    with open(path.join(DataPath, 'maps/projects.dat'), "r") as file:
        projects = [f.strip().split() for f in file.readlines()[2:]]
    for p in projects:
        if p[0] in pdict:
            pdict[p[0]].append(p[1])
        else:
            pdict[p[0]] = [p[1]]
    return pdict

def componentClass():
    datafiles = ['resistors.dat', 'inductors.dat', 'capacitors.dat', 'transistors.dat']
    comps = dict()
    for filename in datafiles:
        with open(path.join(DataPath, 'maps/' + filename), 'r') as file:


def componentList(circuit):
    with open(path.join(DataPath, 'circuits/circuit_' + circuit + '.dat')) as file:
        data = [f.strip() for f in file.readlines()]
    return data[data.index('Components:') + 2:]


def getComponentCountByProject(projectID, componentSymbol):
    cdict = circuitDict(); comps = set()
    if not projectID in cdict:
        raise ValueError('ProjectID ' + projectID + ' not in use.')
    for c in cdict[projectID]:
        None
    componentList(cdict[projectID][0])
    return






if __name__ == "__main__":
    print(getComponentCountByProject('082D6241-40EE-432E-A635-65EA8AA374B6', ""))
