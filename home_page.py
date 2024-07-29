# home_page.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QFrame, QLineEdit
)
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.connection = connection
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Title Frame
        title_frame = QFrame(self)
        title_frame.setFrameShape(QFrame.StyledPanel)
        title_frame.setStyleSheet("""
                QFrame {
                    border: none;
                }
            """)
        title_frame.setFixedHeight(40)

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # back button
        back_button = QPushButton(" << ", self)
        back_button.setStyleSheet("""
            QPushButton {
                color: rgba(165, 137, 120, 0.8);
                font-size: 24px;
                border: none;
            }
            QPushButton:hover {
                color: rgba(87, 71, 64, 0.8);
            }
        """)
        back_button.setFixedHeight(40)
        back_button.clicked.connect(self.go_back)

        # Title
        title_label = QLabel("Home Page", self)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: rgba(165, 137, 120, 0.8);
            padding: 5px 0px;
        """)
        title_label.setFixedHeight(40)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.addWidget(back_button)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addWidget(title_frame)

        # Database information display
        db_info_frame = QFrame(self)
        db_info_frame.setFrameShape(QFrame.StyledPanel)
        db_info_layout = QHBoxLayout(db_info_frame)
        db_info_layout.setContentsMargins(0, 0, 0, 0)

        db_list_frame = QFrame(self)
        db_list_frame.setFrameShape(QFrame.StyledPanel)
        db_list_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 5px;
                padding: 10px;
                border: none;
            }
        """)
        db_list_layout = QVBoxLayout(db_list_frame)
        db_list_layout.setContentsMargins(0, 0, 0, 0)
        db_list_layout.setSpacing(10)

        db_list_label = QLabel("Database name", self)
        db_list_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: rgba(165, 137, 120, 0.8);
            margin: 5px 40px;
        """)
        db_list_label.setFixedHeight(40)
        db_list_layout.addWidget(db_list_label)

        self.db_buttons = []
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        for db in databases:
            db_button = QPushButton(db[0], self)
            db_button.setStyleSheet("""
                QPushButton {
                    background-color: #a58978;
                    color: #ffffff;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 40px;
                    margin: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #574740;
                }
            """)
            db_button.clicked.connect(self.on_db_button_clicked)
            self.db_buttons.append(db_button)
            db_list_layout.addWidget(db_button)

        cursor.close()

        db_info_layout.addWidget(db_list_frame)

        # Select information display
        select_db_frame = QFrame(self)
        select_db_frame.setFrameShape(QFrame.StyledPanel)
        select_db_layout = QVBoxLayout(select_db_frame)
        select_db_label = QLabel("Selected database:", self)
        select_db_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: rgba(165, 137, 120, 0.8);
            padding: 0px;
        """)
        select_db_layout.addWidget(select_db_label)

        self.db_textbox = QLineEdit(self)
        select_db_layout.addWidget(self.db_textbox)

        connect_button = QPushButton("Connect", self)
        connect_button.clicked.connect(self.connect_to_db)
        connect_button.setStyleSheet("""
            QPushButton {
                background-color: #a58978;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #574740;
            }
        """)
        select_db_layout.addWidget(connect_button)

        db_info_layout.addWidget(select_db_frame)

        main_layout.addWidget(db_info_frame)

    def on_db_button_clicked(self):
        sender = self.sender()
        selected_db = sender.text()
        self.db_textbox.setText(selected_db)

    def connect_to_db(self):
        selected_db = self.db_textbox.text()
        QMessageBox.information(self, "Database Selected", f"You have selected {selected_db} database.")
        # Here you can implement further actions, such as updating the connection to use the selected database

    def go_back(self):
        self.parentWidget().setCurrentWidget(self.parentWidget().widget(0))
