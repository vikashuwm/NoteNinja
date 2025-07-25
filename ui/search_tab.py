from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


class NotesSearchTab(QWidget):
    def __init__(self, notes_manager):
        super().__init__()
        self.notes_manager = notes_manager
        self.init_ui()
        self.refresh_notes_list()

    def init_ui(self):
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # 🌈 Pastel + glass theme
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
                margin-right: 10px;
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
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(0, 210, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(58, 71, 213, 0.3);
            }
            QListWidget {
                background-color: rgba(255, 255, 255, 0.6);
                border: none;
                border-radius: 10px;
                padding: 8px;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.65);
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: #333;
            }
        """
        self.setStyleSheet(style)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search your notes...")
        self.search_bar.textChanged.connect(self.search_notes)
        self.search_bar.setMinimumHeight(36)
        top_layout.addWidget(self.search_bar)

        # Optional browser-style icon buttons
        browser_icons = {
            "Chrome": "assets/icons/chrome.png",
            "Firefox": "assets/icons/firefox.png",
            "Edge": "assets/icons/edge.png",
            "Safari": "assets/icons/safari.png"
        }

        for name, path in browser_icons.items():
            if not QIcon(path).isNull():
                btn = QPushButton()
                btn.setToolTip(name)
                btn.setIcon(QIcon(path))
                btn.setIconSize(QSize(22, 22))
                btn.setFlat(True)
                btn.setEnabled(False)  # Placeholder
                top_layout.addWidget(btn)

        # Notes list and preview area
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.display_note)

        self.note_preview = QTextEdit()
        self.note_preview.setReadOnly(True)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.notes_list)
        splitter.addWidget(self.note_preview)
        splitter.setSizes([300, 600])

        # Delete Button
        self.delete_button = QPushButton("🗑️ Delete Selected Note")
        self.delete_button.setEnabled(False)
        self.delete_button.setMinimumHeight(34)
        self.delete_button.clicked.connect(self.delete_note)

        # Layout composition
        layout.addLayout(top_layout)
        layout.addWidget(splitter)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        self.setLayout(layout)

    def refresh_notes_list(self):
        self.notes_list.clear()
        notes = self.notes_manager.get_all_notes()

        for note_data in notes:
            item = QListWidgetItem(f"{note_data['title']} - {note_data['date']}")
            item.setData(Qt.UserRole, note_data)
            self.notes_list.addItem(item)

    def search_notes(self):
        search_term = self.search_bar.text().lower()
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            note_data = item.data(Qt.UserRole)
            title_match = search_term in note_data['title'].lower()
            content_match = search_term in note_data['content'].lower()
            item.setHidden(not (title_match or content_match or not search_term))

    def display_note(self, item):
        note_data = item.data(Qt.UserRole)
        self.note_preview.setPlainText(note_data['content'])
        self.delete_button.setEnabled(True)

    def delete_note(self):
        current_item = self.notes_list.currentItem()
        if current_item:
            note_data = current_item.data(Qt.UserRole)
            reply = QMessageBox.question(
                self,
                "Delete Note",
                f"Are you sure you want to delete \"{note_data['title']}\"?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.notes_manager.delete_note(note_data['filename'])
                self.refresh_notes_list()
                self.note_preview.clear()
                self.delete_button.setEnabled(False)
