from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox
from PyQt5.QtGui import QFont

class TextEditorTab(QWidget):
    def __init__(self, notes_manager):
        super().__init__()
        self.notes_manager = notes_manager
        self.current_filename = None
        self.init_ui()

    def init_ui(self):
        # Apply pastel + glass style similar to NotesSearchTab
        style = """
            QWidget {
                background-color: #e8faff;
            }
            QLineEdit {
                border: none;
                border-radius: 20px;
                padding: 10px 16px;
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
                border-radius: 12px;
                background-color: rgba(255, 255, 255, 0.5);
                padding: 6px 16px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(0, 210, 255, 0.3);
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
                border-radius: 12px;
                padding: 14px;
                font-size: 14px;
                color: #333;
                font-family: Arial, sans-serif;
            }
        """
        self.setStyleSheet(style)

        layout = QVBoxLayout()

        # Toolbar with buttons
        toolbar_layout = QHBoxLayout()
        self.new_button = QPushButton("New")
        self.save_button = QPushButton("Save")
        self.save_pdf_button = QPushButton("Save as PDF")
        self.clear_button = QPushButton("Clear")

        self.new_button.clicked.connect(self.new_note)
        self.save_button.clicked.connect(self.save_note)
        self.save_pdf_button.clicked.connect(self.save_as_pdf)
        self.clear_button.clicked.connect(self.clear_editor)

        toolbar_layout.addWidget(self.new_button)
        toolbar_layout.addWidget(self.save_button)
        toolbar_layout.addWidget(self.save_pdf_button)
        toolbar_layout.addWidget(self.clear_button)
        toolbar_layout.addStretch()

        # Title input with label
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter note title...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)

        # Text editor area
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Start typing your note here...")
        self.text_editor.setFont(QFont("Arial", 12))

        layout.addLayout(toolbar_layout)
        layout.addLayout(title_layout)
        layout.addWidget(self.text_editor)

        # Margins and spacing for a nice layout
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        self.setLayout(layout)

    def new_note(self):
        self.title_input.clear()
        self.text_editor.clear()
        self.current_filename = None

    def save_note(self):
        title = self.title_input.text() or "Untitled"
        content = self.text_editor.toPlainText()

        if not content.strip():
            QMessageBox.warning(self, "Warning", "Cannot save empty note!")
            return

        filename = self.notes_manager.save_note(title, content, self.current_filename)
        self.current_filename = filename
        QMessageBox.information(self, "Success", f"Note saved successfully!")

    def save_as_pdf(self):
        title = self.title_input.text() or "Untitled"
        content = self.text_editor.toPlainText()

        if not content.strip():
            QMessageBox.warning(self, "Warning", "Cannot save empty note as PDF!")
            return

        success = self.notes_manager.save_as_pdf(title, content)
        if success:
            QMessageBox.information(self, "Success", "Note saved as PDF successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to save PDF!")

    def clear_editor(self):
        reply = QMessageBox.question(
            self,
            'Clear Editor',
            'Are you sure you want to clear the editor?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.new_note()
