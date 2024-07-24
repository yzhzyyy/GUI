# mysql_connector_app.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import mysql.connector
from mysql.connector import Error
from database_selection_window import DatabaseSelectionWindow

class MySQLConnectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MySQL Connector')
        self.layout = QVBoxLayout()

        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText('Enter Host')
        self.layout.addWidget(self.host_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText('Enter User')
        self.layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.connect_to_db)
        self.layout.addWidget(self.connect_button)

        self.setLayout(self.layout)

    def connect_to_db(self):
        host = self.host_input.text()
        user = self.user_input.text()
        password = self.password_input.text()

        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )

            if self.connection.is_connected():
                self.open_database_selection_window()
        except Error as e:
            QMessageBox.critical(self, 'Connection Error', f'Error connecting to MySQL database: {e}')

    def open_database_selection_window(self):
        self.db_selection_window = DatabaseSelectionWindow(self.connection, self)
        self.db_selection_window.show()
        self.hide()
