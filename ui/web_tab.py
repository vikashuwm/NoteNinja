from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class WebViewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        nav_layout = QHBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.navigate_to_url)

        self.back_button = QPushButton("Back")
        self.forward_button = QPushButton("Forward")
        self.refresh_button = QPushButton("Refresh")

        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.go_button)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://www.google.com"))

        self.back_button.clicked.connect(self.web_view.back)
        self.forward_button.clicked.connect(self.web_view.forward)
        self.refresh_button.clicked.connect(self.web_view.reload)
        self.web_view.urlChanged.connect(self.update_url_bar)

        layout.addLayout(nav_layout)
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.web_view.setUrl(QUrl(url))

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())
