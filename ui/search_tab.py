import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QToolButton, QListWidget, QSplitter, QMenu,
    QAction, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt, QSize, QPoint, QFileSystemWatcher, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from docx import Document


class NotesSearchTab(QWidget):
    def __init__(self):
        super().__init__()
        self.database_folder = "database"
        self.processed_folder = "opencv"
        self.watcher = QFileSystemWatcher([self.database_folder, self.processed_folder])
        self.watcher.directoryChanged.connect(self.load_all_lists)

        self.init_ui()
        self.load_all_lists()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        style = """
            QWidget {
                background-color: #e8faff;
            }
            QLineEdit {
                border: none;
                border-radius: 20px;
                padding-left: 36px;
                padding-right: 50px;
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
            }
            QToolButton:hover {
                background-color: rgba(0, 210, 255, 0.2);
                border-radius: 10px;
            }
            QListWidget {
                background-color: #eeeeee;
                border: none;
                border-radius: 10px;
                padding: 8px;
            }
            QLabel#processed_label {
                font-weight: bold;
                padding-left: 5px;
                padding-top: 8px;
                padding-bottom: 2px;
            }
        """
        self.setStyleSheet(style)

        # Search bar with icons
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search your notes...")
        self.search_bar.setMinimumHeight(36)
        self.search_bar.textChanged.connect(self.filter_notes_only)

        self.search_button = QToolButton(self.search_bar)
        icon = QIcon.fromTheme("system-search")
        if icon.isNull():
            icon = QIcon("assets/search.png") if QIcon("assets/search.png").availableSizes() else QIcon.fromTheme("edit-find")
        self.search_button.setIcon(icon)
        self.search_button.setIconSize(QSize(16, 16))
        self.search_button.setCursor(Qt.ArrowCursor)
        self.search_button.setFixedSize(20, 20)
        self.search_button.setToolTip("Keyword based search")

        self.context_search_button = QToolButton(self.search_bar)
        icon2 = QIcon("assets/search2.png") if QIcon("assets/search2.png").availableSizes() else QIcon.fromTheme("edit-find")
        self.context_search_button.setIcon(icon2)
        self.context_search_button.setIconSize(QSize(16, 16))
        self.context_search_button.setCursor(Qt.PointingHandCursor)
        self.context_search_button.setFixedSize(20, 20)
        self.context_search_button.setToolTip("Contextual search")
        self.context_search_button.clicked.connect(self.context_search_clicked)

        # Notes list
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_note_content)
        self.notes_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.notes_list.customContextMenuRequested.connect(self.show_context_menu)

        # Processed data
        self.processed_label = QLabel("Processed Data")
        self.processed_label.setObjectName("processed_label")

        self.processed_list = QListWidget()
        self.processed_list.setMaximumHeight(80)
        self.processed_list.itemClicked.connect(self.load_processed_content)
        self.processed_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.processed_list.customContextMenuRequested.connect(self.show_processed_context_menu)

        # Left layout
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(0, 0, 0, 0)
        left_panel_layout.setSpacing(6)
        left_panel_layout.addWidget(self.notes_list, 1)
        left_panel_layout.addWidget(self.processed_label)
        left_panel_layout.addWidget(self.processed_list, 0)

        left_container = QWidget()
        left_container.setLayout(left_panel_layout)

        # Right panel using QWebEngineView
        self.note_viewer = QWebEngineView()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_container)
        splitter.addWidget(self.note_viewer)
        splitter.setSizes([300, 600])

        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(splitter)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.search_button.move(8, (self.search_bar.height() - 20) // 2)
        self.context_search_button.move(self.search_bar.width() - 28, (self.search_bar.height() - 20) // 2)

    def load_all_lists(self):
        self.load_notes()
        self.load_processed()

    def load_notes(self):
        self.notes_list.clear()
        if not os.path.exists(self.database_folder):
            os.makedirs(self.database_folder)

        supported_exts = (".txt", ".docx", ".pdf", ".html", ".htm", ".md", ".json", ".csv")
        for filename in sorted(os.listdir(self.database_folder)):
            if filename.lower().endswith(supported_exts) and not filename.startswith("."):
                self.notes_list.addItem(filename)

    def load_processed(self):
        self.processed_list.clear()
        if not os.path.exists(self.processed_folder):
            os.makedirs(self.processed_folder)

        for filename in sorted(os.listdir(self.processed_folder)):
            if not filename.startswith("."):
                self.processed_list.addItem(filename)

    def filter_notes_only(self):
        term = self.search_bar.text().lower()
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            item.setHidden(term not in item.text().lower())

    def load_note_content(self, item):
        filename = item.text()
        file_path = os.path.join(self.database_folder, filename)
        ext = os.path.splitext(filename)[1].lower()

        try:
            if ext in [".html", ".htm", ".pdf"]:
                self.note_viewer.load(QUrl.fromLocalFile(os.path.abspath(file_path)))

            elif ext in [".txt", ".md", ".json", ".csv"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                html = f"<pre style='font-family: monospace; white-space: pre-wrap;'>{content}</pre>"
                self.note_viewer.setHtml(html)

            elif ext == ".docx":
                doc = Document(file_path)
                content = "<br>".join(p.text for p in doc.paragraphs)
                html = f"<div style='font-family: sans-serif; padding:10px;'>{content}</div>"
                self.note_viewer.setHtml(html)

            else:
                self.note_viewer.setHtml("<h3>Unsupported file format</h3>")

        except Exception as e:
            error_html = f"<h3>Failed to load file:</h3><p>{str(e)}</p>"
            self.note_viewer.setHtml(error_html)

    def load_processed_content(self, item):
        filename = item.text()
        self.note_viewer.setHtml(f"<h3>Processed File Selected</h3><p>{filename}</p>")

    def show_context_menu(self, position: QPoint):
        item = self.notes_list.itemAt(position)
        if item:
            menu = QMenu()
            delete_action = QAction("🗑️ Delete", self)
            delete_action.triggered.connect(lambda: self.delete_file(item.text(), self.database_folder))
            menu.addAction(delete_action)
            menu.exec_(self.notes_list.viewport().mapToGlobal(position))

    def show_processed_context_menu(self, position: QPoint):
        item = self.processed_list.itemAt(position)
        if item:
            menu = QMenu()
            delete_action = QAction("🗑️ Delete", self)
            delete_action.triggered.connect(lambda: self.delete_file(item.text(), self.processed_folder))
            menu.addAction(delete_action)
            menu.exec_(self.processed_list.viewport().mapToGlobal(position))

    def delete_file(self, filename, folder):
        file_path = os.path.join(folder, filename)
        reply = QMessageBox.question(
            self, "Delete File",
            f"Are you sure you want to delete:\n{filename}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                self.load_all_lists()
                self.note_viewer.setHtml("")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete file:\n{e}")

    def context_search_clicked(self):
        self.note_viewer.setHtml("<h3>Contextual search button clicked.</h3>")
