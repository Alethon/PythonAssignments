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

#catalog of components
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

#matches student names to student IDs
def studentIDIndex():
    studentDict = {}
    with open(path.join(DataPath, 'maps/students.dat'), 'r') as file:
        enrolled = [[wd.strip() for wd in f.split('|')] for f in file.readlines()[2:]]
    for student in enrolled:
        studentDict[student[0]] = student[1]
    return studentDict

#matches IDs to student names
def studentNameIndex():
    studentDict = {}
    with open(path.join(DataPath, 'maps/students.dat'), 'r') as file:
        enrolled = [[wd.strip() for wd in f.split('|')] for f in file.readlines()[2:]]
    for student in enrolled:
        studentDict[student[1]] = student[0]
    return studentDict

def componentList(circuitID):
    with open(path.join(DataPath, 'circuits/circuit_' + circuitID + '.dat')) as file:
        data = [f.strip() for f in file.readlines()]
    return data[data.index('Components:') + 2:]

#dictionary that looks up participating students in a circuitID
def getStudentsByCircuit():
    studentDict = {}
    for filename in os.listdir(path.join(DataPath, 'circuits')):
        with open(path.join(DataPath, 'circuits/' + filename), 'r') as file:
            data = [f.strip() for f in file.readlines()[2:]]
        data = data[0:data.index('Components:') - 1]
        studentDict[filename.split('_')[1].split('.')[0]] = data
    return studentDict

#dictionary that looks up circuitIDs a student is participating in
def getCircuitsByStudent():
    studentDict = {}
    for filename in os.listdir(path.join(DataPath, 'circuits')):
        with open(path.join(DataPath, 'circuits/' + filename), 'r') as file:
            data = [f.strip() for f in file.readlines()[2:]]
        data = data[0:data.index('Components:') - 1]
        circuit = filename.split('_')[1].split('.')[0]
        for student in data:
            if student in studentDict:
                studentDict[student].append(circuit)
            else:
                studentDict[student] = [circuit]
    return studentDict

#problem 1
def getComponentCountByProject(projectID, componentSymbol):
    circDict = circuitProjDict(); comps = set()
    if not projectID in circDict:
        raise ValueError('ProjectID ' + projectID + ' not in use.')
    compDict = componentIndex()[componentSymbol]
    for circuit in circDict[projectID]:
        comps.update(set(componentList(circuit)).intersection(set(compDict)))
    return len(comps)

#problem 2
def getComponentCountByStudent(studentName, componentSymbol):
    enrolled = studentIDIndex()
    if studentName not in enrolled:
        raise ValueError(studentName + ' is not enrolled.')
    circuits = getCircuitsByStudent()
    studentID = enrolled[studentName]
    if studentID not in circuits:
        return 0
    comps = set()
    circuits = circuits[studentID]
    matchingComponents = componentIndex()[componentSymbol].keys()
    for circuit in circuits:
        comps.update(set(componentList(circuit)).intersection(set(matchingComponents)))
    return len(comps)

#problem 3
def getParticipationByStudent(studentName):
    students = studentIDIndex()
    if studentName not in students.keys():
        raise ValueError(studentName + ' is not enrolled.')
    projects = set()
    pdict = projectCircDict()
    circuits = getCircuitsByStudent()[students[studentName]]
    for circuit in circuits:
        projects.update(set(pdict[circuit]))
    return projects

#problem 4
def getParticipationByProject(projectID):
    studentIDs = set()
    pdict = circuitProjDict()
    if projectID not in pdict.keys():
        raise ValueError(projectID + ' is not an active project.')
    circuits = pdict[projectID]
    studCircD = getStudentsByCircuit()
    for circuit in circuits:
        studentIDs.update(set(studCircD[circuit]))
    studentNameDict = studentNameIndex()
    return set([studentNameDict[student] for student in studentIDs])

#problem 5
def getCostOfProjects():
    pdict = circuitProjDict()
    compDex = componentIndex()
    prices = {}
    for k in compDex.keys():
        prices.update(compDex[k])
    for k in pdict.keys():
        pdict[k] = round(sum([round(sum([float(prices[component]) for component in componentList(circuit)]), 2) for circuit in pdict[k]]), 2)
    return pdict

#problem 6
def getProjectByComponent(componentIDs):
    circs = projectCircDict()
    return set([p for c in circs.keys() for p in circs[c] if len(set(componentIDs).intersection(set(componentList(c)))) != 0])

#problem 7
def getCommonByProject(projectID1, projectID2):
    p1C = set(); p2C = set()
    circDict = circuitProjDict();
    if not projectID1 in circDict:
        raise ValueError('ProjectID ' + projectID1 + ' not in use.')
    if not projectID2 in circDict:
        raise ValueError('ProjectID ' + projectID2 + ' not in use.')
    for circuit in circDict[projectID1]:
        p1C.update(set(componentList(circuit)))
    for circuit in circDict[projectID2]:
        p2C.update(set(componentList(circuit)))
    return sorted(list(p1C.intersection(p2C)))

#problem 8
def getComponentReport(componentIDs):
    report = {}
    pdict = circuitProjDict()
    for comp in componentIDs:
        report[comp] = 0
    for k in pdict.keys():
        for circuit in pdict[k]:
            for comp in componentList(circuit):
                if comp in report.keys():
                    report[comp] += 1
    return report

#problem 9
def getCircuitByStudent(studentNames):
    circDict = getCircuitsByStudent()
    studentID = studentIDIndex()
    circuits = set()
    for student in studentNames:
        circuits.update(set(circDict[studentID[student]]))
    return circuits

#problem 10
def getCircuitsByComponent(componentIDs):
    circuitIDs = set()
    for filename in os.listdir(path.join(DataPath, 'circuits')):
        with open(path.join(DataPath, 'circuits/' + filename)) as file:
            data = [f.strip() for f in file.readlines()]
        data = data[data.index('Components:') + 2:]
        if len(set(data).intersection(componentIDs)) > 0:
            print(filename.split('_')[1].split('.')[0])
            circuitIDs.update(set([filename.split('.')[0].split('_')[1]]))
    return circuitIDs


if __name__ == "__main__":
    #with open(path.join(DataPath, 'maps/students.dat'), 'r') as file:
    #    enrolled = [[wd.strip() for wd in f.split('|')] for f in file.readlines()[2:]]
    #print([e[0] for e in enrolled[0:5]])
    #print(getCommonByProject('075A54E6-530B-4533-A2E4-A15226BE588C', '4C5B295B-58E1-4CFB-80DF-88938B9A6300'))
    #print(getComponentReport(set(['WTU-670', 'WTX-053', 'XOT-130'])))
    print(getCircuitsByComponent(set(['RLV-754', 'RMY-042', 'RPF-751'])))#, 'Alexander, Carlos', 'Allen, Amanda', 'Anderson, Debra', 'Bailey, Catherine']))