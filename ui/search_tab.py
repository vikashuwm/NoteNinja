from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QTextEdit, QMessageBox, QSplitter, QToolButton, QPushButton
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


class NotesSearchTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.populate_dummy_notes()

    def init_ui(self):
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        style = """
            QWidget {
                background-color: #e8faff;
            }
            QLineEdit {
                border: none;
                border-radius: 20px;
                padding-left: 14px;
                padding-right: 40px;
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
            QToolButton {
                background: transparent;
                border: none;
                padding: 0px;
                margin-right: 8px;
            }
            QToolButton:hover {
                background-color: rgba(0, 210, 255, 0.2);
                border-radius: 10px;
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

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search your notes...")
        self.search_bar.setMinimumHeight(36)
        self.search_bar.textChanged.connect(self.search_notes)
        top_layout.addWidget(self.search_bar)

        self.search_button = QToolButton(self.search_bar)
        icon = QIcon.fromTheme("system-search")
        if icon.isNull():
            icon = QIcon("assets/go.png") if QIcon("assets/go.png").availableSizes() else QIcon.fromTheme("edit-find")
        self.search_button.setIcon(icon)
        self.search_button.setIconSize(QSize(16, 16))
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.manual_search)
        self.search_button.setFixedSize(24, 24)
        self.search_button.move(self.search_bar.width() - 32, (self.search_bar.height() - 24) // 2)

        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.display_note)

        self.note_preview = QTextEdit()
        self.note_preview.setReadOnly(True)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.notes_list)
        splitter.addWidget(self.note_preview)
        splitter.setSizes([300, 600])

        self.delete_button = QPushButton("🗑️ Delete Selected Note")
        self.delete_button.setEnabled(False)
        self.delete_button.setMinimumHeight(34)
        self.delete_button.clicked.connect(self.delete_note)

        layout.addLayout(top_layout)
        layout.addWidget(splitter)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.search_button.move(self.search_bar.width() - 32, (self.search_bar.height() - 24) // 2)

    def populate_dummy_notes(self):
        self.notes_list.clear()
        self.mock_notes = [
            {'title': 'Shopping List', 'content': 'Milk, Bread, Eggs', 'date': '2025-07-25', 'filename': 'note1.txt'},
            {'title': 'Work Plan', 'content': 'Finish report, email John', 'date': '2025-07-24', 'filename': 'note2.txt'},
            {'title': 'Ideas', 'content': 'Build a PyQt app', 'date': '2025-07-23', 'filename': 'note3.txt'}
        ]
        for note in self.mock_notes:
            item = QListWidgetItem(f"{note['title']} - {note['date']}")
            item.setData(Qt.UserRole, note)
            self.notes_list.addItem(item)

    def search_notes(self):
        search_term = self.search_bar.text().lower()
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            note_data = item.data(Qt.UserRole)
            title_match = search_term in note_data['title'].lower()
            content_match = search_term in note_data['content'].lower()
            item.setHidden(not (title_match or content_match or not search_term))

    def manual_search(self):
        print("Manual search button clicked.")

    def display_note(self, item):
        note_data = item.data(Qt.UserRole)
        self.note_preview.setPlainText(note_data['content'])
        self.delete_button.setEnabled(True)
        print(f"Note selected: {note_data['title']}")

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
                print(f"Deleted note: {note_data['title']}")
                self.notes_list.takeItem(self.notes_list.row(current_item))
                self.note_preview.clear()
                self.delete_button.setEnabled(False)
