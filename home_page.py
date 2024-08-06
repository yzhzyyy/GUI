from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QFrame, QLineEdit, QScrollArea, QVBoxLayout
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class HomePage(QWidget):
    db_selected = pyqtSignal(str)  # Define signal

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

        # Title
        title_label = QLabel("Home Page", self)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #A58978;
            padding: 0px 10px;
        """)
        title_label.setFixedHeight(40)
        title_layout.setContentsMargins(0, 0, 0, 0)
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
                padding: 10px;
                background: #F6F6F1;
                border: none;
            }
        """)
        db_list_layout = QVBoxLayout(db_list_frame)
        db_list_layout.setContentsMargins(0, 0, 0, 0)
        db_list_frame.setFixedWidth(275)
        db_list_layout.setSpacing(0)

        # Database name with icon
        db_name_layout = QHBoxLayout()
        db_name_icon = QLabel(self)
        db_name_icon.setPixmap(
            QPixmap("icons/notebook.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        db_name_label = QLabel("Database name", self)
        db_name_label.setStyleSheet("""
                font-size: 25px;
                font-weight: bold;
                color: #C39E83;
                margin: 0px;
            """)
        db_name_label.setFixedHeight(40)
        db_name_layout.addWidget(db_name_icon)
        db_name_layout.addWidget(db_name_label)
        db_list_layout.addLayout(db_name_layout)

        # Database name list in scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setStyleSheet("QWidget{background-color: #F6F6F1; padding: 0px; margin: 0px;}")
        scroll_area.setWidget(scroll_content)
        scroll_area.setFixedHeight(300)

        self.load_databases(scroll_layout)
        db_list_layout.addWidget(scroll_area)
        db_info_layout.addWidget(db_list_frame)

        # Select information display
        select_db_frame = QFrame(self)
        select_db_frame.setFrameShape(QFrame.StyledPanel)
        select_db_layout = QVBoxLayout(select_db_frame)

        # Information text display
        info_frame = QFrame(self)
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setStyleSheet("""
                    QFrame {
                        background-color: #F6F6F1;
                        border: none;
                        padding: 5px 10px;
                    }
                """)
        info_layout = QVBoxLayout(info_frame)
        info_label = QLabel(
            "<b>In this section</b>, you can <span style='color:#A58978; font-size: 24px;'>SELECT THE DATABASE</span> you want to connect to from the left side. "
            "Alternatively, you can <span style='color:#A58978;'>manually enter the database name</span> on the right side. "
            "Then click the '<span style='color:#A58978;'>Connect</span>' button to establish the connection. "
            "Once the connection is successful, you will be redirected to the table page.",
            self
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
                    font-size: 16px;
                    color: #574740;
                """)
        info_layout.addWidget(info_label)
        select_db_layout.addWidget(info_frame)

        select_db_label = QLabel("Selected database:", self)
        select_db_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #C39E83;
            padding: 0px;
        """)
        select_db_label.setFixedHeight(40)
        select_db_layout.addWidget(select_db_label)

        self.db_textbox = QLineEdit(self)
        self.db_textbox.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.db_textbox.setStyleSheet("""
            QLineEdit {
                background-color: #F6F6F1;
                border: 1px solid #C39E83;
                padding: 5px;
                font-size: 16px;
                color: #574740;
            }
            QLineEdit:focus {
                border: 2px solid #a58978;
            }
        """)
        select_db_layout.addWidget(self.db_textbox)

        connect_button = QPushButton("Connect", self)
        connect_button.clicked.connect(self.connect_to_db)
        connect_button.setStyleSheet("""
            QPushButton {
                background-color: #a58978;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #574740;
            }
        """)
        select_db_layout.addWidget(connect_button)

        db_info_layout.addWidget(select_db_frame)
        main_layout.addWidget(db_info_frame)
        self.setLayout(main_layout)

    def load_databases(self, layout):
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        for db in databases:
            db_label = QLabel(db[0], self)
            db_label.setStyleSheet("""
                QLabel {
                    color: #574740;
                    font-size: 16px;
                    padding: 5px 10px;
                }
                QLabel:hover {
                    background-color: #C39E83;
                    color: #ffffff;
                }
            """)
            db_label.mousePressEvent = lambda event, db=db[0]: self.on_db_label_clicked(db)
            layout.addWidget(db_label)
        cursor.close()

    def on_db_label_clicked(self, db_name):
        self.db_textbox.setText(db_name)

    def connect_to_db(self):
        selected_db = self.db_textbox.text()
        if selected_db:
            self.db_selected.emit(selected_db)  # Emit signal with the selected database name
            QMessageBox.information(self, "Connection Successful", f"Connected to {selected_db} database.\nGo to TableView page for more details :)")
        else:
            QMessageBox.warning(self, "No Database Selected", "Please select or enter a database.")
