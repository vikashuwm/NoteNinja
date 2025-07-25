from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTextEdit, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont


class TextEditorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_filename = None
        self.init_ui()

    def init_ui(self):
        style = """
            QWidget {
                background-color: #e8faff;
            }
            QLineEdit {
                border: none;
                border-radius: 20px;
                padding-left: 14px;
                padding-right: 14px;
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
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.6);
                padding: 8px 16px;
                font-weight: 600;
                font-size: 14px;
                color: #333;
                min-height: 34px;
            }
            QPushButton:hover {
                background-color: rgba(0, 210, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(58, 71, 213, 0.3);
            }
            QLabel {
                font-weight: 600;
                font-size: 14px;
                color: #333;
                margin-right: 8px;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.65);
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: #333;
                font-family: Arial, sans-serif;
            }
        """
        self.setStyleSheet(style)

        layout = QVBoxLayout()

        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.new_button = QPushButton("🆕 New")
        self.save_button = QPushButton("💾 Save")
        self.save_pdf_button = QPushButton("🖨️ Save as PDF")
        self.clear_button = QPushButton("🧹 Clear")

        self.new_button.clicked.connect(self.new_note)
        self.save_button.clicked.connect(self.save_note)
        self.save_pdf_button.clicked.connect(self.save_as_pdf)
        self.clear_button.clicked.connect(self.clear_editor)

        for button in [self.new_button, self.save_button, self.save_pdf_button, self.clear_button]:
            toolbar_layout.addWidget(button)
        toolbar_layout.addStretch()

        # Title input
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter note title...")
        self.title_input.setMinimumHeight(36)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)

        # Text editor
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Start typing your note here...")
        self.text_editor.setFont(QFont("Arial", 12))

        # Assemble layout
        layout.addLayout(toolbar_layout)
        layout.addLayout(title_layout)
        layout.addWidget(self.text_editor)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        self.setLayout(layout)

    def new_note(self):
        print("New note clicked")
        self.title_input.clear()
        self.text_editor.clear()
        self.current_filename = None

    def save_note(self):
        print("Save note clicked")

    def save_as_pdf(self):
        print("Save as PDF clicked")

    def clear_editor(self):
        print("Clear editor clicked")
        reply = QMessageBox.question(
            self,
            'Clear Editor',
            'Are you sure you want to clear the editor?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.new_note()
