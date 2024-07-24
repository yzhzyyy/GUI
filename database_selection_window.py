# database_selection_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton
from table_view_window import TableViewWindow

class DatabaseSelectionWindow(QWidget):
    def __init__(self, connection, previous_window):
        super().__init__()
        self.connection = connection
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Database')
        self.layout = QVBoxLayout()

        self.db_combobox = QComboBox(self)
        self.layout.addWidget(self.db_combobox)

        self.enter_button = QPushButton('Enter Database', self)
        self.enter_button.clicked.connect(self.enter_database)
        self.layout.addWidget(self.enter_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
        self.populate_databases()

    def populate_databases(self):
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        self.db_combobox.addItems([db[0] for db in databases])
        cursor.close()

    def enter_database(self):
        selected_db = self.db_combobox.currentText()
        self.table_view_window = TableViewWindow(self.connection, selected_db, self)
        self.table_view_window.show()
        self.hide()

    def go_back(self):
        self.previous_window.show()
        self.close()
