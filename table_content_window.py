# table_content_window.py

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, \
    QSizePolicy
from PyQt5.QtCore import Qt
from itertools import combinations
import time


class TableContentWindow(QWidget):
    def __init__(self, connection, database, table, columns, previous_window):
        super().__init__()
        self.connection = connection
        self.database = database
        self.table = table
        self.columns = columns
        self.previous_window = previous_window
        self.initUI()
        self.previous_hovered_row = -1

    def initUI(self):
        self.setWindowTitle(f'Contents of {self.table}')
        self.layout = QVBoxLayout()

        self.data_table = QTableWidget(self)
        self.ur_table = QTableWidget(self)

        tables_layout = QHBoxLayout()
        tables_layout.addWidget(self.data_table)
        tables_layout.addWidget(self.ur_table)
        tables_layout.setStretch(0, 1)
        tables_layout.setStretch(1, 1)

        self.layout.addLayout(tables_layout)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.setAlignment(self.back_button, Qt.AlignLeft | Qt.AlignTop)

        self.setLayout(self.layout)
        self.populate_table_contents()

    def populate_table_contents(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        columns_list = ", ".join(self.columns)
        cursor.execute(f"SELECT {columns_list} FROM {self.table}")
        rows = cursor.fetchall()

        # Populate data table
        self.data_table.setColumnCount(len(self.columns))
        self.data_table.setRowCount(len(rows))
        self.data_table.setHorizontalHeaderLabels(self.columns)

        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        # Set alternating row colors 启用交替行颜色显示
        self.data_table.setAlternatingRowColors(True)

        # Adjust column width
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Populate uniqueness ratio table 显示 uniqueness ratio
        all_combinations = [combo for length in range(1, len(self.columns) + 1) for combo in
                            combinations(self.columns, length)]

        self.ur_table.setColumnCount(3)
        self.ur_table.setRowCount(len(all_combinations))
        self.ur_table.setHorizontalHeaderLabels(['Key', 'Uniqueness Ratio', 'Running Time'])

        for row_idx, perm in enumerate(all_combinations):
            ratio, exec_time = self.pmax_uniqueness_ratio_sql(cursor, self.table, perm)
            self.ur_table.setItem(row_idx, 0, QTableWidgetItem(", ".join(perm)))
            self.ur_table.setItem(row_idx, 1, QTableWidgetItem(f"{ratio:.4f}"))
            self.ur_table.setItem(row_idx, 2, QTableWidgetItem(f"{exec_time:.4f}"))

        # Set alternating row colors
        self.ur_table.setAlternatingRowColors(True)

        # Adjust column width
        header = self.ur_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Add hover effect for entire row
        self.data_table.setStyleSheet("""
            QTableWidget::item:hover {
                background-color: lightblue;
            }
            QTableWidget::item:selected {
                background-color: darkblue;
                color: white;
            }
        """)

        self.ur_table.setStyleSheet("""
            QTableWidget::item:hover {
                background-color: lightblue;
            }
            QTableWidget::item:selected {
                background-color: darkblue;
                color: white;
            }
        """)

        cursor.close()


    def pmax_uniqueness_ratio_sql(self, cursor, table_name, columns):
        if not columns:
            return 0, 0
        columns_list = ', '.join([f"`{col}`" for col in columns])
        query = f"""
            SELECT
                ((null_rows + unique_rows) / total_rows) AS uniqueness_ratio
            FROM (
                SELECT
                    (SELECT COUNT(*) FROM {table_name} WHERE {' OR '.join([f"`{col}` IS NULL" for col in columns])}) AS null_rows,
                    (
                        SELECT COUNT(*)
                        FROM (
                            SELECT {columns_list}
                            FROM `{table_name}`
                            WHERE {' AND '.join([f"`{col}` IS NOT NULL" for col in columns])}
                            GROUP BY {columns_list}
                            HAVING COUNT(*) = 1
                        ) AS unique_data
                    ) AS unique_rows,
                    (SELECT COUNT(*) FROM {table_name}) AS total_rows
            ) AS results;
        """
        start_time = time.time()
        cursor.execute(query)
        result = cursor.fetchone()
        execution_time = time.time() - start_time
        ratio = result[0] if result else 0

        return ratio, execution_time

    def go_back(self):
        self.previous_window.show()
        self.close()
