from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox
from PyQt5.QtGui import QFont

class TextEditorTab(QWidget):
    def __init__(self, notes_manager):
        super().__init__()
        self.notes_manager = notes_manager
        self.current_filename = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

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

        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter note title...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)

        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Start typing your note here...")
        self.text_editor.setFont(QFont("Arial", 12))

        layout.addLayout(toolbar_layout)
        layout.addLayout(title_layout)
        layout.addWidget(self.text_editor)

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
