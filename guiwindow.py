import sqlite3
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QPushButton, QLineEdit, QTableWidgetItem, QLabel
import traceback


class Window(QMainWindow):

    def __init__(self, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        super().__init__()

        # Labels
        self.title = 'Database Example'
        self.id_label = QLabel(self)
        self.course_label = QLabel(self)

        # Add Text boxes to GUI

        # Add buttons to gui

        # Windows Tools for manipulating database

        # Setting up UI
        self.setup_ui()

        # Showing Ui
        self.show()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(50, 50, 800, 800)

        # Description positions
        self.id_label.setText('Student ID')
        self.id_label.move(50, 20)

        self.course_label.setText('Course ID')
        self.course_label.move(50, 120)


        # Place text boxes in this section

        # Place buttons in this section

    # Add button connections here