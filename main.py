import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Set app attributes for better scaling
    app = QApplication(sys.argv)
    
    # Set some global fonts and settings
    from PyQt6.QtGui import QFont
    app.setFont(QFont("Segoe UI", 10))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
