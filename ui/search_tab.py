from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QTextEdit, QMessageBox, QSplitter, QToolButton, QPushButton
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
                padding-left: 14px;
                padding-right: 40px; /* Increased padding to accommodate icon */
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
                margin-right: 8px; /* Ensure icon stays within bounds */
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

        # 🔍 Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search your notes...")
        self.search_bar.setMinimumHeight(36)
        self.search_bar.textChanged.connect(self.search_notes)
        top_layout.addWidget(self.search_bar)

        # Icon inside QLineEdit
        self.search_button = QToolButton(self.search_bar)
        # Try to load the icon, with a fallback
        icon = QIcon.fromTheme("system-search")
        if icon.isNull():  # Fallback if system theme icon is not available
            try:
                icon = QIcon("assets/go.png")  # Ensure this path is correct
            except:
                # Ultimate fallback: use a default Qt icon
                icon = QIcon.fromTheme("edit-find")
        self.search_button.setIcon(icon)
        self.search_button.setIconSize(QSize(16, 16))
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.manual_search)

        # Position the icon inside the QLineEdit
        self.search_button.setFixedSize(24, 24)  # Ensure button size fits icon
        self.search_button.move(self.search_bar.width() - 32, (self.search_bar.height() - 24) // 2)

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reposition the icon when the search bar is resized
        self.search_button.move(self.search_bar.width() - 32, (self.search_bar.height() - 24) // 2)

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

    def manual_search(self):
        print("Manual search button clicked.")

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