import sqlite3
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QRadioButton, QMessageBox
import pandas as pd


class Employee:

    def __init__(self):
        self.employeeID = 0
        self.fname = "none"
        self.lname = "none"
        self.title = "none"
        self.active = 0
        self.can_order = 0

    def to_string(self):
        print("Employee fname:", self.fname)
        print("Employee lname:", self.lname)
        print("Employee title:", self.title)
        print("Employee active:", self.active)
        print("Employee can_order:", self.can_order)


class Window(QMainWindow):

    def __init__(self, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        super().__init__()

        # Labels
        self.title = 'Database Example'
        self.name_tb = QLabel(self)
        self.title_tb = QLabel(self)
        self.id_tb = QLabel(self)
        self.radio_desc = QLabel(self)

        # Pop ups
        self.id_error = QMessageBox(self)
        self.id_error.setWindowTitle("ID Error")
        self.id_error.setText("The ID you have entered is invalid. Please enter a valid ID")

        self.name_error = QMessageBox(self)
        self.name_error.setWindowTitle("Name Error")
        self.name_error.setText("The name you have entered is invalid. Please enter a valid name.")

        self.title_error = QMessageBox(self)
        self.title_error.setWindowTitle("Title Error")
        self.title_error.setText("The title you have entered is invalid. Please enter a valid name.")

        self.duplicate_entry = QMessageBox(self)
        self.duplicate_entry.setWindowTitle("Duplicate Entry Error")
        self.duplicate_entry.setText("That employee ID already exists in the database.")

        self.show_data = QMessageBox(self)
        self.show_data.setWindowTitle("Current Database")

        # Add Text boxes to GUI
        self.employee_id = QLineEdit(self)
        self.name = QLineEdit(self)
        self.title = QLineEdit(self)

        # Add buttons to gui
        self.reorder = QRadioButton(self)
        self.add_employee = QPushButton(self)
        self.show_employees = QPushButton(self)
        self.show_inventory = QPushButton(self)
        self.ordered_items = QPushButton(self)

        # Database tools
        self.cursor = curs
        self.connection = conn

        # Setting up UI
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Test DB")
        self.setGeometry(50, 50, 800, 800)

        # Description positions
        self.name_tb.setText('Employee Name')
        self.name_tb.resize(180, 30)
        self.name_tb.move(50, 50)

        self.title_tb.setText('Employee Title')
        self.title_tb.resize(180, 30)
        self.title_tb.move(50, 130)

        self.id_tb.setText('Employee ID')
        self.id_tb.move(50, 210)
        self.id_tb.resize(180, 30)

        # Place text boxes in this section
        self.name.move(50, 80)
        self.name.resize(180, 40)

        self.title.move(50, 160)
        self.title.resize(180, 40)

        self.employee_id.move(50, 240)
        self.employee_id.resize(180, 40)

        # Place buttons in this section
        self.add_employee.setText("Add Employee")
        self.add_employee.move(50, 400)
        self.add_employee.resize(180, 40)
        self.reorder.move(50, 300)
        self.reorder.resize(320, 30)
        self.reorder.setText("Check if reorder permissions.")

        self.show_employees.setText("Show Employees")
        self.show_employees.move(50, 450)
        self.show_employees.resize(180, 40)

        self.show_inventory.setText("Show Inventory")
        self.show_inventory.move(50, 500)
        self.show_inventory.resize(180, 40)

        self.ordered_items.setText("Items Ordered")
        self.ordered_items.move(50, 550)
        self.ordered_items.resize(180, 40)

        self.add_employee.clicked.connect(self.add_employee_clicked)
        self.show_employees.clicked.connect(self.select_from)
        self.show_inventory.clicked.connect(self.select_inventory)
        self.ordered_items.clicked.connect(self.get_ordered_items)

        # Showing Ui
        self.show()

    # Add employee button connections
    def add_employee_clicked(self):
        new_employee = Employee()
        try:
            # THIS IS LIST COMPREHENSION
            # IF RUNNING OUT OF TIME IGNORE THIS STEP AND JUST PUSH INFO INTO DB
            # IF ON TIME GLOSS OVER THE IDEA AND MENTION THAT WE CAN GO MORE IN DEPTH ON FRIDAY IN OFFICE HOURS
            if self.employee_id.text().isnumeric() and all((x.isalpha() or x.isspace()) for x in self.name.text()) \
                    and all((x.isalpha() or x.isspace()) for x in self.title.text()):
                new_employee.employeeID = self.employee_id.text()
                new_employee.title = self.title.text()
                names = self.name.text().split(" ")
                try:
                    new_employee.fname = names[0]
                    new_employee.lname = names[1]
                except IndexError:
                    new_employee.fname = self.name.text()
                    new_employee.lname = "NONE"
                if self.reorder.isChecked():
                    new_employee.can_order = 1
                new_employee.active = 1
            else:
                if not self.employee_id.text().isnumeric():
                    self.id_error.exec()
                elif not self.name.text().isalpha():
                    self.name_error.exec()
                else:
                    self.title_error.exec()

            try:
                self.cursor.execute("""INSERT INTO employees (employeeID, fname, lname, title, active, reorder) VALUES
                (?,?,?,?,?,?)""", (new_employee.employeeID, new_employee.fname,
                                   new_employee.lname, new_employee.title,
                                   new_employee.active, new_employee.can_order))
            except Exception as e:
                self.duplicate_entry.exec()

        except Exception as e:
            print(Exception, e)

    def select_from(self):
        try:
            self.cursor.execute("""SELECT * FROM employees""")
            fetched_data = {'Employee ID': [], 'First Name': [], 'Last Name': [],
                            'Title': [], 'Active': [], 'Can Order?':[]}
            for item in self.cursor.fetchall():
                fetched_data['Employee ID'].append(item[0])
                fetched_data['First Name'].append(item[1])
                fetched_data['Last Name'].append(item[2])
                fetched_data['Title'].append(item[3])
                fetched_data['Active'].append(item[4])
                fetched_data['Can Order?'].append(item[5])
            dataframe = pd.DataFrame.from_dict(fetched_data)
            print(dataframe.to_string())
        except Exception as e:
            print(Exception, e)

    def select_inventory(self):
        try:
            self.cursor.execute("""SELECT * FROM inventory""")
            fetched_data = {'Item ID': [], 'Item Description': [], 'Quantity': [],
                            'Restock Ordered': [], 'Ordered By': []}
            for item in self.cursor.fetchall():
                fetched_data['Item ID'].append(item[0])
                fetched_data['Item Description'].append(item[1])
                fetched_data['Quantity'].append(item[2])
                fetched_data['Restock Ordered'].append(item[3])
                fetched_data['Ordered By'].append(item[4])
            dataframe = pd.DataFrame.from_dict(fetched_data)
            print(dataframe.to_string())

        except Exception as e:
            print(Exception, e)

    def get_ordered_items(self):
        try:
            self.cursor.execute("""SELECT employeeID, fname, lname, item_description, quantity
                                   FROM employees INNER JOIN inventory ON inventory.ordered_by = employees.employeeID""")
            fetched_data = {"Employee ID": [], "First Name": [], "Last Name": [], "Item Description": [],
                            "Quantity on Hand": []}

            for item in self.cursor.fetchall():
                fetched_data['Employee ID'].append(item[0])
                fetched_data['First Name'].append(item[1])
                fetched_data['Last Name'].append(item[2])
                fetched_data['Item Description'].append(item[3])
                fetched_data['Quantity on Hand'].append(item[4])

            dataframe = pd.DataFrame.from_dict(fetched_data)
            print(dataframe.to_string())

        except Exception as e:
            print(Exception, e)