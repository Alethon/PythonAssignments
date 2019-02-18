#######################################################
#    Author:      Jacob Laster
#    email:       jlaster
#    ID:          ee364e08
#    Date:        2/17/19
#######################################################

import os
import re
from uuid import UUID

# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab06')

def getUrlParts(url):
    return re.match(r"http://([\w\.\-]*?)/([\w\.\-]*?)/([\w\.\-]*?)\?.*$", url, flags=re.ASCII).groups()

def getQueryParameters(url):
    return re.findall(r"(?P<field>[\w\-\.]+)\=(?P<value>[\w\-\.]+)", url, flags=re.ASCII)

def getSpecial(sentence, letter):
    expression = re.compile(r"\b([^\s{}][\w]*{}|{}[\w]*[^\s{}])\b".format(letter, letter, letter, letter), flags=re.I)
    return re.findall(expression, sentence)

def getRealMac(sentence):
    expression = re.compile(r"\b([a-f\d]{2}:[a-f\d]{2}:[a-f\d]{2}:[a-f\d]{2}:[a-f\d]{2}:[a-f\d]{2}|[a-f\d]{2}-[a-f\d]{2}-[a-f\d]{2}-[a-f\d]{2}-[a-f\d]{2}-[a-f\d]{2})\b", flags=re.I)
    m = re.search(expression, sentence)
    if m is None:
        return None
    else:
        return m.group(0)

def getRejectedEntries():
    names = []
    with open(os.path.join(DataPath, 'Employees.txt'), 'r') as file:
        data = file.readlines()
    nameExpression = re.compile(r"\A((?P<name>[a-z]+ [a-z]+)|(?P<last>[a-z]+), (?P<first>[a-z]+))(?=\b)", flags=re.I)
    eIDExpression = re.compile(r"({?[a-f\d]{8}\-?[a-f\d]{4}\-?[a-f\d]{4}\-?[a-f\d]{4}\-?[a-f\d]{12}}?)", flags=re.I)
    for l in data:
        eID = re.search(eIDExpression, l)
        if eID is None:
            name = re.match(nameExpression, l)
            if name.group('name') is None:
                name = name.group('first') + ' ' + name.group('last')
            else:
                name = name.group('name')
            names.append(name)
    return sorted(names)

def getEmployeesWithIDs():
    res = {}
    with open(os.path.join(DataPath, 'Employees.txt'), 'r') as file:
        data = file.readlines()
    nameExpression = re.compile(r"\A((?P<name>[a-z]+ [a-z]+)|(?P<last>[a-z]+), (?P<first>[a-z]+))(?=\b)", flags=re.I)
    eIDExpression = re.compile(r"({?[a-f\d]{8}\-?[a-f\d]{4}\-?[a-f\d]{4}\-?[a-f\d]{4}\-?[a-f\d]{12}}?)", flags=re.I)
    for l in data:
        eID = re.search(eIDExpression, l)
        if eID is not None:
            name = re.match(nameExpression, l)
            if name.group('name') is None:
                name = name.group('first') + ' ' + name.group('last')
            else:
                name = name.group('name')
            res[name] = str(UUID(eID.group(1)))
    return res

def getEmployeesWithoutIDs():
    names = []
    with open(os.path.join(DataPath, 'Employees.txt'), 'r') as file:
        data = file.readlines()
    nameExpression = re.compile(r"\A((?P<name>[a-z]+ [a-z]+)|(?P<last>[a-z]+), (?P<first>[a-z]+))(?=\b)", flags=re.I)
    eIDExpression = re.compile(r"({?[a-f\d]{8}\-?[a-f\d]{4}\-?[a-f\d]{4}\-?[a-f\d]{4}\-?[a-f\d]{12}}?)", flags=re.I)
    for l in data:
        eID = re.search(eIDExpression, l)
        if eID is None:
            name = re.match(nameExpression, l)
            if name.group('name') is None:
                name = name.group('first') + ' ' + name.group('last')
            else:
                name = name.group('name')
            names.append(name)
    return sorted(names)

def getEmployeesWithPhones():
    res = {}
    with open(os.path.join(DataPath, 'Employees.txt'), 'r') as file:
        data = file.readlines()
    nameExpression = re.compile(r"\A((?P<name>[a-z]+ [a-z]+)|(?P<last>[a-z]+), (?P<first>[a-z]+))(?=\b)", flags=re.I)
    phoneExpression = re.compile(r"(?=\((\d{3})\)? ?\-?(\d{3})\-?(\d{3}))")
    for l in data:
        phone = re.search(phoneExpression, l)
        if phone is not None:
            name = re.match(nameExpression, l)
            if name.group('name') is None:
                name = name.group('first') + ' ' + name.group('last')
            else:
                name = name.group('name')
            res[name] = '(' + phone.group(1) + ') ' + phone.group(2) + '-' + phone.group(3)
    return res

def getEmployeesWithStates():
    res = {}
    with open(os.path.join(DataPath, 'Employees.txt'), 'r') as file:
        data = file.readlines()
    expression = re.compile(r"\A(?P<name>(?P<full>[a-z]+ [a-z]+)|(?P<last>[a-z]+), (?P<first>[a-z]+))[ ,;].*?(?P<state>[a-z]+ ?[a-z]*)$", flags=re.I)
    for l in data:
        m = re.match(expression, l)
        if m is not None and m.group('state') is not None:
            if m.group('name') is None:
                name = m.group('first') + ' ' + m.group('last')
            else:
                name = m.group('name')
            res[name] = m.group('state')
    return res

def getCompleteEntries():
    eIDs = getEmployeesWithIDs()
    phones = getEmployeesWithPhones()
    states = getEmployeesWithStates()
    res = {}
    employees = set(eIDs.keys()).intersection(set(phones.keys())).intersection(set(states.keys()))
    for employee in employees:
        res[employee] = eIDs[employee], phones[employee], states[employee]
    return res

if __name__ == '__main__':
    s = "An example of a MAC address is58-1c-0A-6E-39-4D"
    #getEntries()
    rtn = getCompleteEntries()
    print(rtn)
