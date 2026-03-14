from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QStackedWidget, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from ui.sidebar import Sidebar
from ui.form1 import Form1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Utility Dashboard")
        self.setMinimumSize(1100, 750)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.menu_clicked.connect(self.on_menu_change)
        main_layout.addWidget(self.sidebar)

        # Main Content Area
        content_container = QWidget()
        content_container.setObjectName("content_container")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Title/Header Area
        self.header_label = QLabel("Dashboard")
        self.header_label.setObjectName("header_label")
        content_layout.addWidget(self.header_label)

        # Stacked Widget for Pages
        self.pages = QStackedWidget()
        
        # Placeholder Dashboard
        dashboard_page = self.create_placeholder_page("Dashboard Overview")
        self.pages.addWidget(dashboard_page)

        # Form 1
        self.form1 = Form1()
        self.pages.addWidget(self.form1)

        # Placeholder Form 2
        form2_page = self.create_placeholder_page("Form 2 - Placeholder")
        self.pages.addWidget(form2_page)

        # Placeholder Form 3
        form3_page = self.create_placeholder_page("Form 3 - Placeholder")
        self.pages.addWidget(form3_page)

        # Placeholder Settings
        settings_page = self.create_placeholder_page("Settings")
        self.pages.addWidget(settings_page)

        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_container)

    def create_placeholder_page(self, title):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel(title)
        label.setStyleSheet("font-size: 24px; color: #666;")
        card_layout.addWidget(label)
        
        layout.addWidget(card)
        layout.addStretch()
        return page

    def on_menu_change(self, key):
        menu_map = {
            "dashboard": (0, "Dashboard"),
            "form1": (1, "Form 1 - Database Query"),
            "form2": (2, "Form 2"),
            "form3": (3, "Form 3"),
            "settings": (4, "Settings")
        }
        
        index, title = menu_map.get(key, (0, "Dashboard"))
        self.pages.setCurrentIndex(index)
        self.header_label.setText(title)

    def apply_styles(self):
        # QSS Style Sheet
        style = """
            QMainWindow {
                background-color: #F5F7FB;
            }
            
            #sidebar {
                background-color: #1E1E2F;
                border: none;
            }
            
            #sidebar_logo {
                color: #FFFFFF;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
                margin-bottom: 20px;
            }
            
            QPushButton {
                background-color: transparent;
                color: #A0A0B0;
                border: none;
                text-align: left;
                padding-left: 25px;
                font-size: 14px;
                font-weight: 500;
                border-left: 3px solid transparent;
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.05);
                color: #FFFFFF;
            }
            
            QPushButton:checked {
                background-color: rgba(74, 108, 247, 0.1);
                color: #4A6CF7;
                border-left: 3px solid #4A6CF7;
            }
            
            #content_container {
                background-color: #F5F7FB;
            }
            
            #header_label {
                font-size: 24px;
                font-weight: bold;
                color: #1E1E2F;
            }
            
            #card {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            
            QLineEdit {
                padding: 5px 12px;
                border-radius: 6px;
                border: 1px solid #D0D0D0;
                background-color: #FFFFFF;
                font-size: 13px;
            }
            
            QLineEdit:focus {
                border: 1px solid #4A6CF7;
            }
            
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #444;
            }
            
            #primary_btn {
                background-color: #4A6CF7;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px 15px;
                text-align: center;
            }
            
            #primary_btn:hover {
                background-color: #3D5BD4;
            }
            
            #secondary_btn {
                background-color: #E0E0E0;
                color: #444;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px 15px;
                text-align: center;
            }
            
            #secondary_btn:hover {
                background-color: #D0D0D0;
            }
            
            #accent_btn {
                background-color: #28A745;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px 15px;
                text-align: center;
            }
            
            #accent_btn:hover {
                background-color: #218838;
            }
            
            QTableWidget {
                border: none;
                background-color: #FFFFFF;
                gridline-color: #F0F0F0;
                alternate-background-color: #FAFAFA;
                selection-background-color: rgba(74, 108, 247, 0.1);
                selection-color: #4A6CF7;
                border-radius: 8px;
            }
            
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F0F0F0;
            }
            
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: bold;
                color: #555;
                text-align: left;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #F1F1F1;
                width: 8px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #C1C1C1;
                min-height: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #A1A1A1;
            }
            
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            
            QProgressBar::chunk {
                background-color: #4A6CF7;
            }
        """
        self.setStyleSheet(style)
