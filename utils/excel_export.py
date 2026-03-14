import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QMessageBox

class ExcelExporter:
    @staticmethod
    def export_table_to_excel(table_widget, parent=None):
        """
        Exports data from a QTableWidget to an Excel file using pandas and openpyxl.
        """
        row_count = table_widget.rowCount()
        col_count = table_widget.columnCount()
        
        if row_count == 0:
            QMessageBox.warning(parent, "No Data", "There is no data to export.")
            return

        headers = []
        for i in range(col_count):
            headers.append(table_widget.horizontalHeaderItem(i).text())

        data = []
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = table_widget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)

        df = pd.DataFrame(data, columns=headers)
        
        file_name, _ = QFileDialog.getSaveFileName(
            parent,
            "Save Excel Report",
            "report.xlsx",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_name:
            try:
                df.to_excel(file_name, index=False, engine='openpyxl')
                QMessageBox.information(parent, "Success", f"Data exported successfully to:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(parent, "Export Error", f"Failed to export data:\n{str(e)}")
