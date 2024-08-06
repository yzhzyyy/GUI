import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox,
    QLabel, QTextEdit, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import mysql.connector
from mysql.connector import Error
from main_window import DatabaseSelectionWindow


class MySQLConnectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.default_host = 'localhost'
        self.default_user = 'root'
        self.default_password = '123456'
        self.populate_defaults()

    def initUI(self):

        self.setWindowTitle('MySQL Connector')
        self.setGeometry(100, 100, 800, 400)  # 增大窗口尺寸
        self.setStyleSheet("background-color: #F9FBF5;")

        main_layout = QHBoxLayout()

        # Left Side: Software Description
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)

        # Title
        title_container = QWidget()
        title_layout = QVBoxLayout()
        title_container.setLayout(title_layout)

        title_label = QLabel("Welcome to MySQL Connector")
        title_font = QFont("Arial", 24, QFont.Bold)  # 增大字号
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #574740;")
        title_layout.addWidget(title_label)

        left_layout.addWidget(title_container, alignment=Qt.AlignCenter)

        # Software Description
        description_container = QWidget()
        description_layout = QVBoxLayout()
        description_container.setLayout(description_layout)

        description = QTextEdit(self)
        description.setReadOnly(True)
        description.setFrameStyle(QFrame.NoFrame)
        description.setText("MySQL Connector is a tool that allows you to connect to a MySQL database "
                            "and perform various database operations. Please enter your credentials below to connect.")
        description.setStyleSheet("background-color: #F9FBF5; color: #574740; font-size: 18px;")
        description_layout.addWidget(description)

        left_layout.addWidget(description_container, alignment=Qt.AlignCenter)

        main_layout.addLayout(left_layout)

        # Right Side: Input Form
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)  # Center align the contents

        container = QWidget()
        container_layout = QVBoxLayout()
        container.setFixedSize(300, 200)  # 固定容器大小
        container.setLayout(container_layout)

        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText('Enter Host Name')
        self.style_input(self.host_input)
        self.host_input.setAttribute(Qt.WA_MacShowFocusRect, 0)  # Remove macOS focus rect
        container_layout.addWidget(self.host_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText('Enter User Name')
        self.style_input(self.user_input)
        self.user_input.setAttribute(Qt.WA_MacShowFocusRect, 0)  # Remove macOS focus rect
        container_layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.style_input(self.password_input)
        self.password_input.setAttribute(Qt.WA_MacShowFocusRect, 0)  # Remove macOS focus rect
        container_layout.addWidget(self.password_input)

        # Connect Button
        connect_button = QPushButton('Connect', self)
        connect_button.setFixedSize(100, 40)
        connect_button.setStyleSheet("""
            QPushButton {
                background-color: #574740;
                color: #ffffff;
                font-size: 14px;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b9b7a8;
                color: #574740;
            }
        """)
        connect_button.clicked.connect(self.connect_to_db)
        container_layout.addWidget(connect_button, alignment=Qt.AlignCenter)

        right_layout.addWidget(container)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def style_input(self, input_field):
        input_field.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #574740;
                background-color: #F9FBF5;
                padding: 5px;
                font-size: 14px;
                color: #574740;
                outline: none;
            }
            QLineEdit:hover {
                border: none;
                border-bottom: 2px solid #b9b7a8;
                outline: none;
                color: #574740;
            }
            QLineEdit:focus {
                border: none;
                border-bottom: 2px solid #b9b7a8;
                outline: none;
                color: #574740;
            }
        """)

    def populate_defaults(self):
        self.host_input.setText(self.default_host)
        self.user_input.setText(self.default_user)
        self.password_input.setText(self.default_password)

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
                self.open_database_selection_window(user)
        except Error as e:
            QMessageBox.critical(self, 'Connection Error', f'Error connecting to MySQL database: {e}')

    def open_database_selection_window(self, username):
        self.db_selection_window = DatabaseSelectionWindow(self.connection, self, username)
        self.db_selection_window.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MySQLConnectorApp()
    ex.show()
    sys.exit(app.exec_())
