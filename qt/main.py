import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Test")
    button = QPushButton("My test app")
    button.pressed.connect(self.close)
    self.setCentralWidget(button)
    self.show()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  w = MainWindow()
  app.exec()