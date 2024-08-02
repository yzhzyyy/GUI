import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QFrame, QSplitter, QSizePolicy, QSpacerItem, QPushButton, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

from gitclone.key_view_page import KeyViewPage
from table_view_page import TableViewPage
from home_page import HomePage
import mysql.connector

class DatabaseSelectionWindow(QWidget):
    db_selected = pyqtSignal(str)

    def __init__(self, connection, previous_window, username):
        super().__init__()
        self.connection = connection
        self.previous_window = previous_window
        self.username = username
        self.selected_db = None  # Default value for selected_db
        self.selected_table = None  # Default value for selected_table
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MySQL Connector Dashboard')
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #b9b7a8; color: #574740;")

        main_layout = QHBoxLayout(self)

        # Create a splitter for the layout
        splitter = QSplitter(Qt.Horizontal)

        # Create the left navigation area
        nav_widget = QFrame()
        nav_widget.setFixedWidth(200)  # Fixed width for the navigation bar
        nav_layout = QVBoxLayout(nav_widget)

        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                border: none;
            }
            QListWidget::item {
                height: 40px;
                padding-left: 10px;
                outline: none;
                border: none;
            }
            QListWidget::item:hover {
                background-color: #a58978;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #a58978;
                color: #ffffff;
            }
        """)
        self.home_item = self.create_nav_item("Home", "icons/home.png")
        self.tableview_item = self.create_nav_item("Table View", "icons/table.png")
        self.keyview_item = self.create_nav_item("Key View", "icons/database.png")
        self.blank_item = self.create_nav_item("Blank", "icons/key_analysis.png")

        self.nav_list.addItem(self.home_item)
        self.nav_list.addItem(self.tableview_item)
        self.nav_list.addItem(self.keyview_item)
        self.nav_list.addItem(self.blank_item)
        self.nav_list.itemClicked.connect(self.on_nav_item_clicked)
        nav_layout.addWidget(self.nav_list)

        # Add spacer to push user info to the bottom
        nav_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add user icon at the top
        user_icon = QLabel(self)
        user_icon.setPixmap(
            QPixmap("icons/portrait.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        user_icon.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(user_icon)

        # Add user info at the bottom
        self.user_info_label = QLabel(f"User: {self.username}\nDatabase: {self.selected_db}")
        self.user_info_label.setAlignment(Qt.AlignCenter)
        self.user_info_label.setStyleSheet("color: #ffffff; font-size: 14px")
        nav_layout.addWidget(self.user_info_label)

        # Add logout button at the bottom
        logout_button = QPushButton('Logout', self)
        logout_button.setStyleSheet("""
                    QPushButton {
                        color: #ffffff;
                        border: 2px solid #ffffff;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #a58978;
                    }
                """)
        logout_button.clicked.connect(self.logout)
        nav_layout.addWidget(logout_button)

        splitter.addWidget(nav_widget)

        # Create the right content area
        self.content_area = QFrame()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_area.setStyleSheet("background-color: #FFFFFF; border: none;")
        self.content_label = QLabel("Welcome to MySQL Connector Dashboard", self.content_area)
        self.content_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #574740;")
        self.content_layout.addWidget(self.content_label)
        splitter.addWidget(self.content_area)

        # Set the sizes for the splitter
        splitter.setSizes([200, 800])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Set default selection to Home
        self.nav_list.setCurrentItem(self.home_item)
        self.on_nav_item_clicked(self.home_item)

    def create_nav_item(self, text, icon_path):
        item = QListWidgetItem(text)
        item.setIcon(QIcon(icon_path))
        return item

    def logout(self):
        self.previous_window.show()
        self.close()

    def on_nav_item_clicked(self, item):
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if item.text() == "Home":
            home_page = HomePage(self.connection, self.content_area)
            home_page.db_selected.connect(self.set_selected_db)  # Connect signal
            self.content_layout.addWidget(home_page)
            print(self.selected_db)

        elif item.text() == "Table View":
            if self.selected_db is not None:
                table_view_page = TableViewPage(self.connection, self.content_area, self.selected_db)
                table_view_page.table_selected.connect(self.set_selected_table)  # Connect signal
                self.content_layout.addWidget(table_view_page)
            else:
                QMessageBox.warning(self, "No Database Selected", "Please select a database from the Home page first.")

        elif item.text() == "Key View":
            if self.selected_db and self.selected_table:
                self.content_layout.addWidget(
                    KeyViewPage(self.connection, self.content_area, self.selected_db, self.selected_table))
            else:
                QMessageBox.warning(self, "No Table Selected",
                                    "Please select a table from the Table View page first.")

        elif item.text() == "Blank":
            self.content_label = QLabel("Blank Page", self.content_area)
            self.content_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #574740;")
            self.content_layout.addWidget(self.content_label)

    def set_selected_db(self, db_name):
        self.selected_db = db_name
        self.user_info_label.setText(f"User: {self.username}\nDatabase: {self.selected_db}")

    def set_selected_table(self, table_name):
        self.selected_table = table_name
