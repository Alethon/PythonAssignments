#######################################################
#    Author:      Jacob Laster
#    email:       jlaster
#    ID:          ee364e08
#    Date:        1/23/19
#######################################################

import os
import sys

# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab03')

#circuits and maps
def listDir():
    return [f for f in os.listdir(DataPath) if os.path.isfile(os.path.join(DataPath, f))]

def getComponentCountByProject(projectID, componentSymbol):
    with open(os.path.join(DataPath, 'maps/projects.dat'), "r") as file:
        projects = file.readlines()
    print(projects[0:10])
    if not os.path.isfile(os.path.join(DataPath, 'circuits' + projectID + '.dat')):
        raise ValueError('Team does not exist.')
    return






if __name__ == "__main__":
    print(getComponentCountByProject('', ""))