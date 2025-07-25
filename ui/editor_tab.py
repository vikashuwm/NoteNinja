from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QMessageBox, QFileDialog
)
from PyQt5.QtGui import (
    QFont, QIcon, QTextCharFormat, QTextCursor,
    QTextImageFormat, QPixmap
)
from PyQt5.QtCore import QSize, Qt
import os


class ImageTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        if source.hasImage():
            image = source.imageData()
            if image:
                cursor = self.textCursor()
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaledToWidth(300, Qt.SmoothTransformation)
                image_name = f'image_{id(image)}.png'
                scaled_pixmap.save(image_name, "PNG")

                image_format = QTextImageFormat()
                image_format.setName(image_name)
                image_format.setWidth(scaled_pixmap.width())
                image_format.setHeight(scaled_pixmap.height())
                cursor.insertImage(image_format)
        else:
            super().insertFromMimeData(source)


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
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.65);
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: #333;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 210, 255, 0.2);
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: rgba(58, 71, 213, 0.3);
                border-radius: 10px;
            }
        """
        self.setStyleSheet(style)

        layout = QVBoxLayout()
        toolbar_layout = QHBoxLayout()
        icon_path = "assets"

        # Buttons
        self.new_button = self.create_button(icon_path, "new.png", "New Note", self.new_note)
        self.open_button = self.create_button(icon_path, "open.png", "Open Note", self.open_note)
        self.save_button = self.create_button(icon_path, "save.png", "Save Note", self.save_note)
        self.clear_button = self.create_button(icon_path, "clear.png", "Clear Editor", self.clear_editor)
        self.undo_button = self.create_button(icon_path, "undo.png", "Undo", self.text_editor_undo)
        self.bold_button = self.create_button(icon_path, "bold.png", "Bold Selected Text", self.toggle_bold)
        self.image_button = self.create_button(icon_path, "camera.png", "Insert Image from File", self.insert_image_from_file)

        for btn in [
            self.new_button, self.open_button, self.save_button, self.clear_button,
            self.undo_button, self.bold_button, self.image_button
        ]:
            toolbar_layout.addWidget(btn)
            btn.setIconSize(QSize(24, 24))

        toolbar_layout.addStretch()

        # Text Editor
        self.text_editor = ImageTextEdit()
        self.text_editor.setPlaceholderText("Start typing your note here...")
        self.text_editor.setFont(QFont("Arial", 12))

        layout.addLayout(toolbar_layout)
        layout.addWidget(self.text_editor)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        self.setLayout(layout)

    def create_button(self, path, icon_file, tooltip, callback):
        button = QPushButton()
        button.setIcon(QIcon(os.path.join(path, icon_file)))
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        return button

    def new_note(self):
        self.text_editor.clear()
        self.current_filename = None

    def open_note(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Note", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_editor.setText(content)
                    self.current_filename = file_path
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open file:\n{str(e)}")

    def save_note(self):
        if self.current_filename is None:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Note", "", "Text Files (*.txt);;All Files (*)"
            )
            if not file_path:
                return
            self.current_filename = file_path

        try:
            with open(self.current_filename, "w", encoding="utf-8") as file:
                file.write(self.text_editor.toPlainText())
                QMessageBox.information(self, "Saved", "Note saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save file:\n{str(e)}")

    def clear_editor(self):
        reply = QMessageBox.question(
            self, 'Clear Editor', 'Are you sure you want to clear the editor?',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.new_note()

    def text_editor_undo(self):
        self.text_editor.undo()

    def toggle_bold(self):
        cursor = self.text_editor.textCursor()
        if not cursor.hasSelection():
            return

        fmt = QTextCharFormat()
        current_weight = cursor.charFormat().fontWeight()
        fmt.setFontWeight(QFont.Normal if current_weight == QFont.Bold else QFont.Bold)
        cursor.mergeCharFormat(fmt)
        self.text_editor.mergeCurrentCharFormat(fmt)

    def insert_image_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Insert Image", "", "Images (*.png *.jpg *.bmp *.gif);;All Files (*)"
        )
        if file_path:
            cursor = self.text_editor.textCursor()
            pixmap = QPixmap(file_path)
            scaled = pixmap.scaledToWidth(300, Qt.SmoothTransformation)

            image_format = QTextImageFormat()
            image_format.setName(file_path)
            image_format.setWidth(scaled.width())
            image_format.setHeight(scaled.height())
            cursor.insertImage(image_format)
