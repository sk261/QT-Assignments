import sys
from PySide2.QtUiTools import QUiLoader #allows us to import .ui files
from PySide2.QtWidgets import QApplication, QLineEdit, QCheckBox
from PySide2.QtCore import QFile, QObject

class MainWindow(QObject):

    #class constructor
    def __init__(self, ui_file, parent=None):

        #call parent QObject constructor
        super(MainWindow, self).__init__(parent)

        self.binaryVals = [0,0,0]

        #load the UI file into Python
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        
        #always remember to close files
        ui_file.close()

        for i in [1, 2]:
            for n in range(8):
                box = self.window.findChild(QCheckBox, 'Reactant' + str(i) + '_' + str(n+1))
                box.toggled.connect(self.boxChecked)
                
        self.window.Summation.toggled.connect(self.boxChecked)
        self.window.Multiplication.toggled.connect(self.boxChecked)
        self.window.Division.toggled.connect(self.boxChecked)
        self.window.Subtraction.toggled.connect(self.boxChecked)

        self.window.Clear.clicked.connect(self.clear)
        
        for n in list(range(8))[::-1]:
            box = self.window.findChild(QCheckBox, 'Product_' + str(n+1))
            box.toggled.connect(self.blockInput)
        
        self.write()

        #show window to user
        self.window.show()

    def clear(self):
        self.binaryVals = [0, 0, 0]
        for i in [1, 2]:
            for n in range(8):
                box = self.window.findChild(QCheckBox, 'Reactant' + str(i) + '_' + str(n+1))
                box.setChecked(False)
        self.write()

    
    def write(self):
        # Write the values
        self.window.Reactant1Decimal.setText(str(self.binaryVals[0]))
        self.window.Reactant2Decimal.setText(str(self.binaryVals[1]))
        self.window.ProductDecimal.setText(str(self.binaryVals[2]))

        # Check all the right boxes
        result = self.binaryVals[2]
        for n in list(range(8))[::-1]:
            box = self.window.findChild(QCheckBox, 'Product_' + str(n+1))
            r = result >= 2 ** n
            box.setChecked(r)
            if r:
                result -= 2 ** n
    
    def blockInput(self, a):
        self.write()
    
    def boxChecked(self):
        for i in [0, 1]:
            self.binaryVals[i] = 0
            for n in list(range(8))[::-1]:
                box = self.window.findChild(QCheckBox, 'Reactant' + str(i+1) + '_' + str(n+1))
                if box.isChecked():
                    self.binaryVals[i] += 2 ** n
        
        result = 0
        if self.window.Summation.isChecked():
            result = self.binaryVals[0] + self.binaryVals[1]
        elif self.window.Multiplication.isChecked():
            result = self.binaryVals[0] * self.binaryVals[1]
        elif self.window.Division.isChecked():
            result = int(self.binaryVals[0] / self.binaryVals[1])
        elif self.window.Subtraction.isChecked():
            result = self.binaryVals[0] - self.binaryVals[1]
        
        # Cut off anything above the last bit
        result %= 256
        self.binaryVals[2] = result

        self.write()

        


    def seven_button_clicked(self):
        print(self.window.Reactant1_1.isChecked())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('ShaysQTCalculator.ui')
    sys.exit(app.exec_())

