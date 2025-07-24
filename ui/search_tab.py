from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTextEdit, QMessageBox, QSplitter
from PyQt5.QtCore import Qt

class NotesSearchTab(QWidget):
    def __init__(self, notes_manager):
        super().__init__()
        self.notes_manager = notes_manager
        self.init_ui()
        self.refresh_notes_list()

    def init_ui(self):
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search through your notes...")
        self.search_bar.textChanged.connect(self.search_notes)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_notes)

        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.display_note)

        self.note_preview = QTextEdit()
        self.note_preview.setReadOnly(True)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.notes_list)
        splitter.addWidget(self.note_preview)
        splitter.setSizes([300, 500])

        self.delete_button = QPushButton("Delete Selected Note")
        self.delete_button.clicked.connect(self.delete_note)
        self.delete_button.setEnabled(False)

        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        layout.addWidget(splitter)
        layout.addWidget(self.delete_button)
        layout.addLayout(search_layout)

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
                'Delete Note',
                f'Are you sure you want to delete "{note_data["title"]}"?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.notes_manager.delete_note(note_data['filename'])
                self.refresh_notes_list()
                self.note_preview.clear()
                self.delete_button.setEnabled(False)
