from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, 
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon

class SidebarButton(QPushButton):
    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Placeholder for icons - in a real app, use QIcon("assets/icons/...")
        # if icon_name:
        #     self.setIcon(QIcon(f"assets/icons/{icon_name}.png"))
        #     self.setIconSize(QSize(20, 20))

class Sidebar(QWidget):
    menu_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setObjectName("sidebar")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)

        # Logo/Title
        logo_label = QLabel("DB UTILITY")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setObjectName("sidebar_logo")
        layout.addWidget(logo_label)
        
        layout.addSpacing(30)

        # Menu Items
        self.buttons = {}
        menu_items = [
            ("Dashboard", "dashboard"),
            ("Form 1", "form1"),
            ("Form 2", "form2"),
            ("Form 3", "form3"),
            ("Settings", "settings")
        ]

        for text, key in menu_items:
            btn = SidebarButton(text, key)
            btn.clicked.connect(lambda checked, k=key: self.on_menu_click(k))
            layout.addWidget(btn)
            self.buttons[key] = btn

        layout.addStretch()

        # Set default active
        self.buttons["dashboard"].setChecked(True)

    def on_menu_click(self, key):
        # Uncheck others
        for k, btn in self.buttons.items():
            btn.setChecked(k == key)
        self.menu_clicked.emit(key)
