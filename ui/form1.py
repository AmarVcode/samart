from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QMessageBox, QFrame, QSizePolicy, 
    QAbstractItemView, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QSize
from PyQt6.QtGui import QColor, QFont, QIcon
from database.db_connection import DatabaseConnection
from utils.excel_export import ExcelExporter
import pandas as pd

class DatabaseThread(QThread):
    finished = pyqtSignal(list, str) # results, error_msg

    def __init__(self, yr_id, book_cd):
        super().__init__()
        self.yr_id = yr_id
        self.book_cd = book_cd

    def run(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT a.VchId, a.VchDate, a.TrDrAmt 
                FROM vcdet a 
                WHERE a.YrId = %s AND a.BookCd = %s
            """
            results = db.execute_query(query, (self.yr_id, self.book_cd))
            self.finished.emit(results, "")
        except Exception as e:
            self.finished.emit([], str(e))

class Form1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("form1")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Filter Card
        filter_card = QFrame()
        filter_card.setObjectName("card")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 20, 20, 20)
        filter_layout.setSpacing(15)

        # Inputs
        self.yr_id_input = QLineEdit()
        self.yr_id_input.setPlaceholderText("Year ID (e.g. 2526)")
        self.yr_id_input.setText("2526") # Default for demo
        self.yr_id_input.setFixedWidth(150)
        self.yr_id_input.setFixedHeight(35)

        self.book_cd_input = QLineEdit()
        self.book_cd_input.setPlaceholderText("Book Code (e.g. SLSPH)")
        self.book_cd_input.setText("SLSPH") # Default for demo
        self.book_cd_input.setFixedWidth(150)
        self.book_cd_input.setFixedHeight(35)

        filter_layout.addWidget(QLabel("Year ID:"))
        filter_layout.addWidget(self.yr_id_input)
        filter_layout.addSpacing(10)
        filter_layout.addWidget(QLabel("Book Code:"))
        filter_layout.addWidget(self.book_cd_input)
        filter_layout.addStretch()

        # Buttons
        self.search_btn = QPushButton("Search")
        self.search_btn.setObjectName("primary_btn")
        self.search_btn.setFixedWidth(100)
        self.search_btn.setFixedHeight(35)
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.clicked.connect(self.on_search)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondary_btn")
        self.clear_btn.setFixedWidth(100)
        self.clear_btn.setFixedHeight(35)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.on_clear)

        self.export_btn = QPushButton("Export to Excel")
        self.export_btn.setObjectName("accent_btn")
        self.export_btn.setFixedWidth(140)
        self.export_btn.setFixedHeight(35)
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.clicked.connect(self.on_export)

        filter_layout.addWidget(self.search_btn)
        filter_layout.addWidget(self.clear_btn)
        filter_layout.addWidget(self.export_btn)

        layout.addWidget(filter_card)

        # Loading Spinner Overlay (Simple approach: A progress bar)
        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0) # Indeterminate
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedHeight(3)
        self.loading_bar.hide()
        layout.addWidget(self.loading_bar)

        # Table Grid
        table_container = QFrame()
        table_container.setObjectName("card")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(1, 1, 1, 1)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Voucher ID", "Voucher Date", "Amount"])
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Table Styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        
        table_layout.addWidget(self.table)
        layout.addWidget(table_container)

    def on_search(self):
        yr_id = self.yr_id_input.text().strip()
        book_cd = self.book_cd_input.text().strip()

        if not yr_id or not book_cd:
            QMessageBox.warning(self, "Input Error", "Please enter both Year ID and Book Code.")
            return

        self.loading_bar.show()
        self.search_btn.setEnabled(False)
        self.table.setRowCount(0)

        self.db_thread = DatabaseThread(yr_id, book_cd)
        self.db_thread.finished.connect(self.on_data_loaded)
        self.db_thread.start()

    def on_data_loaded(self, results, error_msg):
        self.loading_bar.hide()
        self.search_btn.setEnabled(True)

        if error_msg:
            QMessageBox.critical(self, "Database Error", error_msg)
            return

        self.table.setRowCount(len(results))
        for row, data in enumerate(results):
            # Voucher ID
            vch_id = QTableWidgetItem(str(data.get('VchId', '')))
            vch_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, vch_id)

            # Voucher Date
            vch_date = QTableWidgetItem(str(data.get('VchDate', '')))
            vch_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, vch_date)

            # Amount
            amt = data.get('TrDrAmt', 0.0)
            amt_item = QTableWidgetItem(f"{float(amt):,.2f}")
            amt_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 2, amt_item)

        if not results:
            QMessageBox.information(self, "No Results", "No records found for the given criteria.")

    def on_clear(self):
        self.yr_id_input.clear()
        self.book_cd_input.clear()
        self.table.setRowCount(0)

    def on_export(self):
        ExcelExporter.export_table_to_excel(self.table, self)
