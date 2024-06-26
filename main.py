from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout,
                             QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog,
                             QToolBar, QStatusBar)
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")
        self.setMinimumSize(800, 600)

        # menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        edit_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_action)

        self.table = QTableWidget() # add table
        self.table.setColumnCount(4) # set number of columns
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))  # set table labels
        self.table.verticalHeader().setVisible(False)  # hide first index column
        self.setCentralWidget(self.table) # specify central widget for window

        # toolbar with insert & search icon
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(edit_action)

        # Create status bar and add status bar items
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Button")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Button")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

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

    def edit(self):
        edit = EditDialog()
        edit.exec()

    def delete(self):
        delete = DeleteDialog()
        delete.exec()

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
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
                       (name,))
        rows = list(result)
        print(rows)
        items = student_management.table.findItems(name, Qt.MatchFlag.MatchFixedString) # match name string
        for item in items:
            print(item)
            student_management.table.item(item.row(), 1).setSelected(True)

        connection.commit()
        cursor.close()
        connection.close()

        # load refreshed data
        student_management.load_data()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # Extract items out of table and selected row
        index = student_management.table.currentRow()
        student_name = student_management.table.item(index, 1).text()
        course_name = student_management.table.item(index, 2).text()
        mobile_no = student_management.table.item(index, 3).text()
        self.id = student_management.table.item(index, 0).text()

        # Add selected student name
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Dropdown selected course
        self.course_name = QComboBox()
        courses = ['Math', 'Astronomy', 'Biology', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add selected mobile no
        self.student_mobile = QLineEdit(mobile_no)
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.student_mobile.text(),
                        self.id))

        connection.commit()
        cursor.close()
        connection.close()

        # load refreshed data
        student_management.load_data()

class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
student_management.load_data()
# Start the event loop.
sys.exit(app.exec())