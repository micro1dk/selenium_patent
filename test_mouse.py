import sys
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGroupBox, QHBoxLayout

 
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5'
        self.left = 150
        self.top = 150
        self.width = 200
        self.height = 200
        self.initUI()
        
    def initUI(self):
        window = QHBoxLayout()
        
        x, y = pyautogui.position()  
        self.text = "x: {0} ,y: {1} ".format(x, y)
        self.label = QLabel(self.text, self)
 
        window.addWidget(self.label)
        self.setLayout(window)
 
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
 
    def mouseMoveEvent(self, pos):
        x, y = pyautogui.position()  
 
        text = "x: {0}, y: {1} ".format(x, y)
        self.label.setText(text)
 
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
