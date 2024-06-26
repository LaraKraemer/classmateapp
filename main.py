from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout,
                             QLineEdit, QPushButton, QComboBox, QMainWindow)
import sys


class MainWindow(QMainWindow):
    pass




app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()