import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QFrame, QSplitter, QSizePolicy, QSpacerItem, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from home_page import HomePage
import mysql.connector

class DatabaseSelectionWindow(QWidget):
    def __init__(self, connection, previous_window, username):
        super().__init__()
        self.connection = connection
        self.previous_window = previous_window
        self.username = username
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
                border-radius: 20px;
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
        self.widgets_item = self.create_nav_item("Widgets", "icons/database.png")
        self.tableview_item = self.create_nav_item("TableView", "icons/table.png")
        self.blank_item = self.create_nav_item("Blank", "icons/key_analysis.png")

        self.nav_list.addItem(self.home_item)
        self.nav_list.addItem(self.widgets_item)
        self.nav_list.addItem(self.tableview_item)
        self.nav_list.addItem(self.blank_item)
        self.nav_list.itemClicked.connect(self.on_nav_item_clicked)
        nav_layout.addWidget(self.nav_list)

        # Add spacer to push user info to the bottom
        nav_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add user info at the bottom
        user_info_label = QLabel(f"User: {self.username}\nDatabase: {self.connection.database}")
        print(self.username)
        user_info_label.setAlignment(Qt.AlignCenter)
        user_info_label.setStyleSheet("color: #ffffff;")
        nav_layout.addWidget(user_info_label)

        # Add logout button at the bottom
        logout_button = QPushButton('Logout', self)
        logout_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(165, 137, 120, 0.8);
                        color: #ffffff;
                        border: none;
                        border-radius: 20px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: rgba(87, 71, 64, 0.8);
                    }
                """)
        logout_button.clicked.connect(self.logout)
        nav_layout.addWidget(logout_button)

        splitter.addWidget(nav_widget)

        # Create the right content area
        self.content_area = QFrame()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_area.setStyleSheet("background-color: #FFFFFF; border-radius: 30px;")
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
            self.content_layout.addWidget(HomePage(self.connection, self.content_area))
        elif item.text() == "Widgets":
            self.content_label = QLabel("Widgets Page", self.content_area)
            self.content_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #574740;")
            self.content_layout.addWidget(self.content_label)
        elif item.text() == "TableView":
            self.content_label = QLabel("Table View Page", self.content_area)
            self.content_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #574740;")
            self.content_layout.addWidget(self.content_label)
        elif item.text() == "Blank":
            self.content_label = QLabel("Blank Page", self.content_area)
            self.content_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #574740;")
            self.content_layout.addWidget(self.content_label)



