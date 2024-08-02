import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal

class TableViewPage(QWidget):
    table_selected = pyqtSignal(str)  # Define signal

    def __init__(self, connection, parent=None, database=None):
        super().__init__(parent)
        self.connection = connection
        self.database = database
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel(f"Tables in Database: {self.database}", self)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #A58978;
            padding: 0px 10px;
        """)
        title_label.setFixedHeight(40)
        main_layout.addWidget(title_label)

        body_widget = QWidget()
        body_layout = QVBoxLayout(body_widget)

        # Upper part: Table selection
        image_path = os.path.abspath("icons/next.png")
        table_selection_layout = QHBoxLayout()
        self.table_combo_box = QComboBox(self)
        self.load_table_names()
        self.table_combo_box.setStyleSheet(f"""
            QComboBox {{
                background-color: #F6F6F1;
                color: #574740;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background: #F6F6F1;
            }}
            QComboBox::down-arrow {{
                image: url("{image_path}");
                width: 13px;
                height: 13px;
            }}
            QComboBox::down-arrow:on {{ 
                top: 1px;
                left: 1px;
            }}
        """)
        table_selection_layout.addWidget(self.table_combo_box, 3)

        select_table_button = QPushButton("Select Table", self)
        select_table_button.clicked.connect(self.on_select_table_button_clicked)
        select_table_button.setStyleSheet("""
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
        table_selection_layout.addWidget(select_table_button)

        body_layout.addLayout(table_selection_layout)

        # Statistics view title
        stats_title_label = QLabel("Statistics View", self)
        stats_title_label.setAlignment(Qt.AlignLeft)
        stats_title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #A58978;
            padding: 10px 0px;
        """)
        body_layout.addWidget(stats_title_label)

        # Statistics view
        self.attribute_stats_widget = QTableWidget(self)
        self.attribute_stats_widget.setColumnCount(6)
        self.attribute_stats_widget.setHorizontalHeaderLabels(["Attribute", "Data Type", "Null Values", "Duplicate Values", "Unique Values", "Total Rows"])
        self.attribute_stats_widget.setStyleSheet("""
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
        self.attribute_stats_widget.setAlternatingRowColors(True)
        body_layout.addWidget(self.attribute_stats_widget, 3)

        main_layout.addWidget(body_widget)
        self.setLayout(main_layout)

        # Default to first table
        self.default_to_first_table()

    def load_table_names(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        self.table_combo_box.clear()
        for table in tables:
            self.table_combo_box.addItem(table[0])

        cursor.close()

    def on_select_table_button_clicked(self):
        selected_table = self.table_combo_box.currentText()
        self.load_table_data(selected_table)
        self.table_selected.emit(selected_table)  # Emit signal with selected table

    def default_to_first_table(self):
        if self.table_combo_box.count() > 0:
            first_table = self.table_combo_box.itemText(0)
            self.load_table_data(first_table)

    def load_table_data(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute(f"SELECT * FROM `{table_name}`")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Get column data types
        cursor.execute(f"DESCRIBE `{table_name}`")
        column_info = cursor.fetchall()
        column_data_types = {info[0]: info[1] for info in column_info}

        self.attribute_stats_widget.setRowCount(len(columns))

        for i, column in enumerate(columns):
            # Get data type
            data_type = column_data_types[column]

            # Get null values count
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}` WHERE `{column}` IS NULL")
            null_count = cursor.fetchone()[0]

            # Get total count
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            total_count = cursor.fetchone()[0]

            # Get unique values count
            cursor.execute(f"SELECT COUNT(DISTINCT `{column}`) FROM `{table_name}`")
            unique_count = cursor.fetchone()[0]

            # Calculate duplicate values count
            duplicate_count = total_count - unique_count

            self.attribute_stats_widget.setItem(i, 0, QTableWidgetItem(column))
            self.attribute_stats_widget.setItem(i, 1, QTableWidgetItem(data_type))
            self.attribute_stats_widget.setItem(i, 2, QTableWidgetItem(str(null_count)))
            self.attribute_stats_widget.setItem(i, 3, QTableWidgetItem(str(duplicate_count)))
            self.attribute_stats_widget.setItem(i, 4, QTableWidgetItem(str(unique_count)))
            self.attribute_stats_widget.setItem(i, 5, QTableWidgetItem(str(total_count)))

        cursor.close()
