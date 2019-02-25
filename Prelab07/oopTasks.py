#######################################################
#    Author:      Jacob Laster
#    email:       jlaster
#    ID:          ee364e08
#    Date:        2/24/19
#######################################################

from enum import Enum

class Level(Enum):
    Freshman = 1
    Sophomore = 2
    Junior = 3
    Senior = 4

class ComponentType(Enum):
    Resistor = 1
    Capacitor = 2
    Inductor = 3
    Transistor = 4

class Student:
    def __str__(self):
        return self.ID + ", " + self.firstName + " " + self.lastName + ", " + self.level.name
    def __init__(self, ID, firstName, lastName, level):
        if level not in Level:
            raise TypeError("The argument must be an instance of the 'Level' Enum.")
        self.ID = ID
        self.firstName = firstName
        self.lastName = lastName
        self.level = level

class Component:
    def __init__(self, ID, ctype, price):
        if ctype not in ComponentType:
            raise TypeError("The argument must be an instance of the 'ComponentType' Enum.")
        self.ID = ID
        self.ctype = ctype
        self.price = price
    def __str__(self):
        return self.ctype.name + ", " + self.ID + ", ${:.02f}".format(self.price)
    def __hash__(self):
        return hash(self.ID)

class Circuit:
    def __init__(self, ID, components):
        self.cost = 0.0
        for component in components:
            if not isinstance(component, Component):
                raise TypeError("The argument must be an instance of the 'Component' class.")
            self.cost += component.price
        self.cost = round(self.cost, 2)
        self.components = components
        self.ID = ID
    def getByType(self, ctype):
        if ctype not in ComponentType:
            raise ValueError("The argument must be an instance of the 'ComponentType' Enum.")
        count = 0
        for component in self.components:
            if component.ctype is ctype:
                count += 1
        return count
    def __str__(self):
        return self.ID + ": (R = {:02d}, C = {:02d}, I = {:02d}, T = {:02d}), Cost = ${:.02f}".format(self.getByType(ComponentType.Resistor),
                                                                                 self.getByType(ComponentType.Capacitor),
                                                                                 self.getByType(ComponentType.Inductor),
                                                                                 self.getByType(ComponentType.Transistor),
                                                                                 self.cost)
    def __contains__(self, item):
        if not isinstance(item, Component):
            raise TypeError("The argument must be an instance of the 'Component' class.")
        if item in self.components:
            return True
        return False
    def __add__(self, item):
        if not isinstance(item, Component):
            raise TypeError("The argument must be an instance of the 'Component' class.")
        if item not in self:
            self.components.add(item)
            self.cost = round(item.price + self.cost, 2)
        return self
    def __radd__(self, item):
        return self + item
    def __sub__(self, item):
        if not isinstance(item, Component):
            raise TypeError("The argument must be an instance of the 'Component' class.")
        if item in self:
            self.components.remove(item)
            self.cost = round( self.cost - item.price, 2)
        return self
    def __gt__(self, item):
        if not isinstance(item, Circuit):
            raise TypeError("The argument must be an instance of the 'Circuit' class.")
        return self.cost > item.cost
    def __lt__(self, item):
        if not isinstance(item, Circuit):
            raise TypeError("The argument must be an instance of the 'Circuit' class.")
        return self.cost < item.cost
    def __eq__(self, item):
        if not isinstance(item, Circuit):
            raise TypeError("The argument must be an instance of the 'Circuit' class.")
        return self.cost == item.cost

class Project:
    def __init__(self, ID, participants, circuits):
        self.cost = 0.0
        for circuit in circuits:
            if not isinstance(circuit, Circuit):
                raise ValueError("The argument must be an instance of the 'Circuit' class.")
            self.cost += circuit.cost
            self[circuit.ID] = circuit
        for participant in participants:
            if not isinstance(participant, Student):
                raise ValueError("The argument must be an instance of the 'Student' class.")
        self.cost = round(self.cost, 2)
        self.circuits = circuits
        self.participants = participants
        self.ID = ID
    def __str__(self):
        return self.ID + ": ({:02d} Circuits, {:02d} Participants), Cost = ${:.02f}".format(len(self.circuits),
                                                                                       len(self.participants),
                                                                                       self.cost)
    def __contains__(self, item):
        if isinstance(item, Component):
            for circuit in self.circuits:
                if item in circuit:
                    return True
            return False
        elif isinstance(item, Circuit):
            if item in self.circuits:
                return True
            return False
        elif isinstance(item, Student):
            if item in self.participants:
                return True
            return False
        else:
            raise TypeError("The argument must be an instance of the 'Component' class, the 'Circuit' class, or the 'Student' class.")
    def __add__(self, item):
        if not isinstance(item, Circuit):
            raise TypeError("The argument must be an instance of the 'Circuit' class.")
        if item not in self.circuits:
            self.circuits.append(item)
            self[item.ID] = item
            self.cost = round(self.cost + item.cost, 2)
        return self
    def __sub__(self, item):
        if not isinstance(item, Circuit):
            raise TypeError("The argument must be an instance of the 'Circuit' class.")
        if item in self.circuits:
            self.circuits.remove(item)
            del self[item.ID]
            self.cost = round(self.cost - item.cost, 2)
        return self
    def __getitem__(self, circuitID):
        if circuitID in self.__dict__.keys():
            return self.__dict__[circuitID]
        raise KeyError("Key does not exist.")
    def __setitem__(self, key, value):
        if isinstance(key, str) and isinstance(value, Circuit) and key not in self.__dict__.keys():
            self.__dict__[key] = value
    def __delitem__(self, key):
        if isinstance(key, str) and key not in ['ID', 'circuits', 'participants', 'cost']:
            del self.__dict__[key]

class Capstone(Project):
    def __init__(self, arg1, *args):
        if not isinstance(arg1, Project) and len(args) == 2:
            participants = args[0]
            circuits = args[1]
            self.cost = 0.0
            for circuit in circuits:
                if not isinstance(circuit, Circuit):
                    raise ValueError("The argument must be an instance of the 'Circuit' class.")
                self.cost += circuit.cost
                self[circuit.ID] = circuit
            for participant in participants:
                if not isinstance(participant, Student):
                    raise ValueError("The argument must be an instance of the 'Student' class.")
                if participant.level is not Level.Senior:
                    raise ValueError("All students must be Seniors.")
            self.cost = round(self.cost, 2)
            self.circuits = circuits
            self.participants = participants
            self.ID = arg1
        elif isinstance(arg1, Project) and len(args) == 0:
            participants = arg1.participants
            circuits = arg1.circuits
            self.cost = 0.0
            for circuit in circuits:
                if not isinstance(circuit, Circuit):
                    raise ValueError("The argument must be an instance of the 'Circuit' class.")
                self.cost += circuit.cost
                self[circuit.ID] = circuit
            for participant in participants:
                if not isinstance(participant, Student):
                    raise ValueError("The argument must be an instance of the 'Student' class.")
                if participant.level is not Level.Senior:
                    raise ValueError("All students must be Seniors.")
            self.cost = round(self.cost, 2)
            self.circuits = circuits
            self.participants = participants
            self.ID = arg1.ID
        else:
            raise ValueError("A capstone could not be constructed from inputs.")





