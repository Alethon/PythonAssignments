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
    return [f for f in os.listdir(path.join(DataPath, 'maps'))]

def circuitProjDict():
    cdict = {}
    with open(path.join(DataPath, 'maps/projects.dat'), "r") as file:
        projects = [f.strip().split() for f in file.readlines()[2:]]
    for p in projects:
        if p[1] in cdict:
            cdict[p[1]].append(p[0])
        else:
            cdict[p[1]] = [p[0]]
    return cdict

def projectCircDict():
    pdict = {}
    with open(path.join(DataPath, 'maps/projects.dat'), "r") as file:
        projects = [f.strip().split() for f in file.readlines()[2:]]
    for p in projects:
        if p[0] in pdict:
            pdict[p[0]].append(p[1])
        else:
            pdict[p[0]] = [p[1]]
    return pdict

def componentIndex():
    comps = {}
    datafiles = ['resistors.dat', 'inductors.dat', 'capacitors.dat', 'transistors.dat']
    for filename in datafiles:
        with open(path.join(DataPath, 'maps/' + filename), 'r') as file:
            data = [[f.strip().split()[0], float(f.strip().split()[1].strip('$'))] for f in file.readlines()[3:]]
        comps[str(filename.upper()[0])] = {}
        for d in data:
            comps[str(filename.upper()[0])][d[0]] = d[1]
    return comps

def componentList(circuit):
    with open(path.join(DataPath, 'circuits/circuit_' + circuit + '.dat')) as file:
        data = [f.strip() for f in file.readlines()]
    return data[data.index('Components:') + 2:]

def getComponentCountByProject(projectID, componentSymbol):
    circDict = circuitProjDict(); comps = set()
    if not projectID in circDict:
        raise ValueError('ProjectID ' + projectID + ' not in use.')
    compDict = componentIndex()[componentSymbol]
    for circuit in circDict[projectID]:
        comps.update(set(componentList(circuit)).intersection(set(compDict)))
    return len(comps)

def getComponentCountByStudent(studentName, componentSymbol):
    with open(path.join(DataPath, 'maps/students.dat'), 'r') as file:
        data = [[wd.strip() for wd in f.split('|')] for f in file.readlines()[2:]]
    return data




if __name__ == "__main__":
    #print(getComponentCountByProject('082D6241-40EE-432E-A635-65EA8AA374B6', "C"))
    #print(getComponentCountByStudent("", "")[5:20])
    print(listDir())