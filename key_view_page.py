import os
import itertools
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QCheckBox, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox, QFrame, QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt

class KeyViewPage(QWidget):
    def __init__(self, connection, parent=None, database=None, table=None):
        super().__init__(parent)
        self.connection = connection
        self.database = database
        self.table = table
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel(f"Key Combinations for Table: {self.table}", self)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #A58978;
            padding: 0px 10px;
        """)
        title_label.setFixedHeight(40)
        main_layout.addWidget(title_label)

        attributes_list_title = QLabel("Attributes List", self)
        attributes_list_title.setAlignment(Qt.AlignLeft)
        attributes_list_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #A58978;
            padding: 10px 0px;
        """)
        main_layout.addWidget(attributes_list_title)

        # Use QScrollArea to make the attributes list resizable
        attributes_scroll_area = QScrollArea(self)
        attributes_scroll_area.setWidgetResizable(True)
        attributes_scroll_area.setFixedHeight(150)

        self.attributes_list = QListWidget(self)
        self.attributes_list.setStyleSheet("""
            QListWidget {
                background-color: #F6F6F1;
                border: none;
                padding: 5px;
            }
            QListWidget::item {
                height: 30px;
                padding-left: 10px;
            }
            QListWidget::item:hover {
                background-color: #a58978;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #F6F6F1;
                color: black;
            }
        """)
        self.load_attributes()
        self.attributes_list.itemClicked.connect(self.toggle_item_check)
        attributes_scroll_area.setWidget(self.attributes_list)
        main_layout.addWidget(attributes_scroll_area)

        calculate_button_layout = QHBoxLayout()
        calculate_button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.calculate_button = QPushButton("Calculate Combinations", self)
        self.calculate_button.clicked.connect(self.calculate_combinations)
        self.calculate_button.setFixedSize(170, 30)
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #a58978;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #574740;
            }
        """)
        calculate_button_layout.addWidget(self.calculate_button)
        main_layout.addLayout(calculate_button_layout)

        # Results view title
        results_title_label = QLabel("Uniqueness Ratio Table", self)
        results_title_label.setAlignment(Qt.AlignLeft)
        results_title_label.setContentsMargins(0, 0, 0, 0)
        results_title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #A58978;
            padding: 10px 0px;
        """)
        main_layout.addWidget(results_title_label)

        # Results table
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Combination", "Uniqueness Ratio", "Running Time"])
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: transparent;
            }
            QTableWidget::item {
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #a58978;
                color: white;
            }
            QHeaderView::section {
                background-color: #f6f6f1;
                color: #574740;
                padding: 5px;
                border: none;
            }
            QTableWidget::item:!selected {
                background-color: #FFFFFF;
            }
            QTableWidget::item:!selected:alternate {
                background-color: #F6F6F1;
            }
        """)
        self.results_table.setAlternatingRowColors(True)
        main_layout.addWidget(self.results_table, 3)

        # Set initial column widths
        self.results_table.setColumnWidth(0, 200)  # Width for the 'Combination' column
        self.results_table.setColumnWidth(1, 150)  # Width for the 'Uniqueness Ratio' column
        self.results_table.setColumnWidth(2, 150)  # Width for the 'Running Time' column

        self.setLayout(main_layout)

    def load_attributes(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute(f"DESCRIBE `{self.table}`")
        attributes = cursor.fetchall()

        self.attributes_list.clear()
        for attribute in attributes:
            item = QListWidgetItem(attribute[0])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.attributes_list.addItem(item)

        cursor.close()

    def toggle_item_check(self, item):
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def calculate_combinations(self):
        selected_attributes = [item.text() for item in self.attributes_list.findItems("*", Qt.MatchWildcard) if item.checkState() == Qt.Checked]
        if len(selected_attributes) > 5:
            QMessageBox.warning(self, "Too Many Attributes Selected", "Please select up to 5 attributes.")
            return

        if not selected_attributes:
            QMessageBox.warning(self, "No Attributes Selected", "Please select at least one attribute.")
            return

        self.results_table.setRowCount(0)
        combinations = self.get_combinations(selected_attributes)

        for combo in combinations:
            ratio, exec_time = self.calculate_uniqueness_ratio(combo)
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            self.results_table.setItem(row_position, 0, QTableWidgetItem(", ".join(combo)))
            self.results_table.setItem(row_position, 1, QTableWidgetItem(f"{ratio:.4f}"))
            self.results_table.setItem(row_position, 2, QTableWidgetItem(f"{exec_time:.4f}"))

    def get_combinations(self, attributes):
        all_combinations = []
        for length in range(1, len(attributes) + 1):
            all_combinations.extend(itertools.combinations(attributes, length))
        return all_combinations

    def calculate_uniqueness_ratio(self, combo):
        cursor = self.connection.cursor()
        start_time = time.time()
        query = f"SELECT COUNT(DISTINCT {', '.join(combo)}) / COUNT(*) FROM {self.table}"
        cursor.execute(query)
        ratio = cursor.fetchone()[0]
        exec_time = time.time() - start_time
        cursor.close()
        return ratio, exec_time
