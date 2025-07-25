import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QMessageBox, QFileDialog
)
from PyQt5.QtGui import (
    QFont, QIcon, QTextCharFormat, QTextCursor,
    QTextImageFormat, QPixmap
)
from PyQt5.QtCore import QSize, Qt


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
            QLabel {
                font-size: 10px;
                color: #333;
            }
        """
        self.setStyleSheet(style)

        layout = QVBoxLayout()
        icon_path = "assets"

        toolbar_layout = QHBoxLayout()

        def create_button_with_label(icon_file, tooltip, callback, label_text):
            button = QPushButton()
            button.setIcon(QIcon(os.path.join(icon_path, icon_file)))
            button.setToolTip(tooltip)
            button.clicked.connect(callback)
            button.setIconSize(QSize(24, 24))
            button.setFixedSize(40, 40)

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedHeight(16)

            v_layout = QVBoxLayout()
            v_layout.setContentsMargins(2, 0, 2, 0)
            v_layout.setSpacing(0)  # reduce spacing here
            v_layout.addWidget(button)
            v_layout.addWidget(label)

            container = QWidget()
            container.setLayout(v_layout)
            return container

        buttons_with_labels = [
            ("new.png", "New Note", self.new_note, "New"),
            ("open.png", "Open Note", self.open_note, "Open"),
            ("save.png", "Save Note", self.save_note, "Save"),
            ("clear.png", "Clear Editor", self.clear_editor, "Clear"),
            ("undo.png", "Undo", self.text_editor_undo, "Undo"),
            ("bold.png", "Bold Selected Text", self.toggle_bold, "Bold"),
            ("camera.png", "Insert Image from File", self.insert_image_from_file, "Image"),
        ]

        for icon_file, tooltip, callback, label_text in buttons_with_labels:
            widget = create_button_with_label(icon_file, tooltip, callback, label_text)
            toolbar_layout.addWidget(widget)

        toolbar_layout.addStretch()

        self.text_editor = ImageTextEdit()
        self.text_editor.setPlaceholderText("Start typing your note here...")
        self.text_editor.setFont(QFont("Arial", 12))

        layout.addLayout(toolbar_layout)
        layout.addWidget(self.text_editor)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        self.setLayout(layout)

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
