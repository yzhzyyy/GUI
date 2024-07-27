import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QIcon
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
        self.setStyleSheet("background-color: #F9FBF5; color: #574740;")

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
                padding-left: 20px;
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
        self.nav_list.addItem(self.create_nav_item("Home", "icons/home.png"))
        self.nav_list.addItem(self.create_nav_item("Widgets", "icons/database.png"))
        self.nav_list.addItem(self.create_nav_item("TableView", "icons/table.png"))
        self.nav_list.addItem(self.create_nav_item("Blank", "icons/key_analysis.png"))
        self.nav_list.itemClicked.connect(self.on_nav_item_clicked)
        nav_layout.addWidget(self.nav_list)

        # Add spacer to push user info to the bottom
        nav_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add user info at the bottom
        user_info_label = QLabel(f"User: {self.username}\nDatabase: {self.connection.database}")
        user_info_label.setAlignment(Qt.AlignCenter)
        user_info_label.setStyleSheet("color: #aaaaaa;")
        nav_layout.addWidget(user_info_label)

        splitter.addWidget(nav_widget)

        # Create the right content area
        self.content_area = QFrame()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_area.setStyleSheet("background-color: #FFFFFF;")
        self.content_label = QLabel("Welcome to MySQL Connector Dashboard", self.content_area)
        self.content_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #574740;")
        self.content_layout.addWidget(self.content_label)
        splitter.addWidget(self.content_area)

        # Set the sizes for the splitter
        splitter.setSizes([200, 800])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def create_nav_item(self, text, icon_path):
        item = QListWidgetItem(text)
        item.setIcon(QIcon(icon_path))
        return item

    def on_nav_item_clicked(self, item):
        if item.text() == "Home":
            self.content_label.setText("Home Page")
        elif item.text() == "Widgets":
            self.content_label.setText("Widgets Page")
        elif item.text() == "TableView":
            self.content_label.setText("Table View Page")
        elif item.text() == "Blank":
            self.content_label.setText("Blank Page")
