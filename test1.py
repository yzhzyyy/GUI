import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QComboBox, QLabel, QTextEdit
)
import mysql.connector
from mysql.connector import Error

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

class TableContentWindow(QWidget):
    def __init__(self, connection, database, table, previous_window):
        super().__init__()
        self.connection = connection
        self.database = database
        self.table = table
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Contents of {self.table}')
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
        self.populate_table_contents()

    def populate_table_contents(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute(f"SELECT * FROM {self.table}")
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        display_text = f"Table: {self.table}\n\n" + "\t".join(column_names) + "\n"
        for row in rows:
            display_text += "\t".join(map(str, row)) + "\n"
        self.text_edit.setPlainText(display_text)
        cursor.close()

    def go_back(self):
        self.previous_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MySQLConnectorApp()
    ex.show()
    sys.exit(app.exec_())
