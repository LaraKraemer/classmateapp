from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout,
                             QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")

        # menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)


        self.table = QTableWidget() # add table
        self.table.setColumnCount(4) # set number of columns
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))  # set table labels
        self.table.verticalHeader().setVisible(False)  # hide first index column
        self.setCentralWidget(self.table) # specify central widget for window


    def load_data(self):
        # connect to database
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        # insert data in gui table
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()



app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
student_management.load_data()
# Start the event loop.
sys.exit(app.exec())