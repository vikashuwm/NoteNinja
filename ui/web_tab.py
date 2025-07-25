from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon


class WebViewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        nav_layout = QHBoxLayout()
        icon_size = QSize(24, 24)

        # 🌈 Pastel + glassmorphic theme (matching NotesSearchTab)
        style = """
            QWidget {
                background-color: #e8faff;
            }
            QLineEdit {
                border: none;
                border-radius: 20px;
                padding-left: 16px;
                padding-right: 16px;
                padding-top: 10px;
                padding-bottom: 10px;
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.7);
                color: #333;
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d2ff, stop:1 #3a47d5
                );
            }
            QPushButton {
                border: none;
                border-radius: 14px;
                background-color: rgba(255, 255, 255, 0.6);
                padding: 6px;
            }
            QPushButton:hover {
                background-color: rgba(0, 210, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(58, 71, 213, 0.3);
            }
            QPushButton:disabled {
                opacity: 0.4;
            }
        """
        self.setStyleSheet(style)

        # Navigation buttons
        icons = [
            ("back", "Back", self.web_view_back),
            ("forward", "Forward", self.web_view_forward),
            ("refresh", "Refresh", self.web_view_reload),
            ("go", "Go", self.navigate_to_url)
        ]
        for name, tip, handler in icons:
            btn = QPushButton()
            btn.setIcon(QIcon(f"assets/{name}.png"))
            btn.setToolTip(tip)
            btn.setIconSize(icon_size)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(handler)
            setattr(self, f"{name}_button", btn)
            nav_layout.addWidget(btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter website...")
        self.url_bar.setMinimumHeight(36)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        nav_layout.insertWidget(3, self.url_bar, 1)
        nav_layout.setSpacing(8)
        nav_layout.setContentsMargins(12, 12, 12, 12)

        # Web View
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://www.google.com"))
        self.web_view.urlChanged.connect(self.update_url_bar)
        self.web_view.setStyleSheet("border: none; background-color: #f8fcff;")

        # Final Layout
        layout.addLayout(nav_layout)
        layout.addWidget(self.web_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def web_view_back(self):
        if self.web_view.history().canGoBack():
            self.web_view.back()

    def web_view_forward(self):
        if self.web_view.history().canGoForward():
            self.web_view.forward()

    def web_view_reload(self):
        self.web_view.reload()

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url if '.' in url else 'https://www.google.com/search?q=' + url.replace(' ', '+')
        self.web_view.setUrl(QUrl(url))

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())
        self.back_button.setEnabled(self.web_view.history().canGoBack())
        self.forward_button.setEnabled(self.web_view.history().canGoForward())
