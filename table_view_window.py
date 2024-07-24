# table_view_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton
from table_content_window import TableContentWindow

class TableViewWindow(QWidget):
    def __init__(self, connection, database, previous_window):
        super().__init__()
        self.connection = connection
        self.database = database
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Select Table in {self.database}')
        self.layout = QVBoxLayout()

        self.table_combobox = QComboBox(self)
        self.layout.addWidget(self.table_combobox)

        self.view_button = QPushButton('View Table', self)
        self.view_button.clicked.connect(self.view_table)
        self.layout.addWidget(self.view_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
        self.populate_tables()

    def populate_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        self.table_combobox.addItems([table[0] for table in tables])
        cursor.close()

    def view_table(self):
        selected_table = self.table_combobox.currentText()
        self.table_content_window = TableContentWindow(self.connection, self.database, selected_table, self)
        self.table_content_window.show()
        self.hide()

    def go_back(self):
        self.previous_window.show()
        self.close()
