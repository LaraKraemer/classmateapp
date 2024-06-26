from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout,
                             QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog)
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
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        edit_action = QAction("Search", self)
        edit_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_action)

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

    def insert(self):
        # generate popup window with dialog method
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        search = SearchDialog()
        search.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add drop down of courses
        self.course_name = QComboBox()
        courses = ['Math', 'Astronomy', 'Biology', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # add mobile widget
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def add_student(self):
        name = self.student_name.text()
        # return choice of user
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        # load refreshed data
        student_management.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # search student name
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name")
        layout.addWidget(self.search_name)

        # submit button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.search_name.text()
        # return choice of user
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = ?",
                       (name))
        connection.commit()
        cursor.close()
        connection.close()

        # load refreshed data
        student_management.load_data()


app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
student_management.load_data()
# Start the event loop.
sys.exit(app.exec())