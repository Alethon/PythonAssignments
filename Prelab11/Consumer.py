
#######################################################
#   Author:     Jacob Laster
#   email:      jlaster
#   ID:         ee364e08
#   Date:       3/31/2019
#######################################################

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from BasicUI import *
from PyQt5.QtWidgets import QLineEdit
import re


class Consumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Consumer, self).__init__(parent)
        self.setupUi(self)
        self.btnSave.setEnabled(False)
        self.chkGraduate.clicked.connect(self.enableSave)
        self.txtStudentName.textChanged.connect(self.enableSave)
        self.txtStudentID.textChanged.connect(self.enableSave)
        self.cboCollege.activated.connect(self.enableSave)
        self.compList = [(self.findChild(QLineEdit, "txtComponentName_" + str(i)), self.findChild(QLineEdit, "txtComponentCount_" + str(i))) for i in range(1, 21)]
        for comp in self.compList:
            comp[0].textChanged.connect(self.enableSave)
            comp[1].textChanged.connect(self.enableSave)
        self.btnClear.clicked.connect(self.clearData)
        self.btnSave.clicked.connect(self.saveData)
        self.btnLoad.clicked.connect(self.loadData)


    def loadData(self):
        """
        *** DO NOT MODIFY THIS METHOD! ***
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        You must modify the method below.
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open XML file ...', filter="XML files (*.xml)")

        if not filePath:
            return

        self.loadDataFromFile(filePath)

    def loadDataFromFile(self, filePath):
        """
        Handles the loading of the data from the given file name. This method will be invoked by the 'loadData' method.
        
        *** YOU MUST USE THIS METHOD TO LOAD DATA FILES. ***
        *** This method is required for unit tests! ***
        """
        with open(filePath, "r") as file:
            data = file.readlines()[2:]
        del data[-1]
        del data[-1]
        s = re.search(r'<StudentName graduate="(?P<graduate>true|false)">(?P<name>.*)</StudentName>\n', data[0])
        if s.group('graduate') == 'true':
            self.chkGraduate.setChecked(True)
        self.txtStudentName.setText(s.group('name'))
        s = re.search(r'<StudentID>(.*)</StudentID>\n', data[1])
        self.txtStudentID.setText(s.group(1))
        s = re.search(r'<College>(.*)</College>\n', data[2])
        self.cboCollege.setCurrentIndex(self.cboCollege.findText(s.group(1)))
        r = re.compile(r'<Component name="(?P<name>.*)" count="(?P<count>.*)" />\n')
        compstr = ""
        for line in data[4:]:
            compstr += line
        s = re.findall(r, compstr)
        index = 0
        while index < 20 and index < len(s):
            self.compList[index][0].setText(s[index][0])
            self.compList[index][1].setText(s[index][1])
            index = index + 1
    
    def clearData(self):
        self.chkGraduate.setCheckState(False)
        self.cboCollege.setCurrentIndex(0)
        self.txtStudentName.clear()
        self.txtStudentID.clear()
        for comp in self.compList:
            comp[0].clear()
            comp[1].clear()
        self.btnSave.setEnabled(False)
        self.btnLoad.setEnabled(True)

    def enableSave(self):
        self.btnSave.setEnabled(True)
        self.btnLoad.setEnabled(False)

    def saveData(self):
        with open("target.xml", "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n<Content>\n')
            file.write('\t<StudentName graduate="' + str(self.chkGraduate.isChecked()).lower() + '">' + self.txtStudentName.text() + '</StudentName>\n')
            file.write('\t<StudentID>' + self.txtStudentID.text() + '</StudentID>\n')
            file.write('\t<College>' + self.cboCollege.currentText() + '</College>\n')
            file.write('\t<Components>\n')
            for line in self.compList:
                if line[0].text() != "" and line[1].text() != "":
                    file.write('\t\t<Component name="' + line[0].text() + '" count="' + line[1].text() + '" />\n')
            file.write('\t</Components>\n')
            file.write('</Content>\n')




if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()
