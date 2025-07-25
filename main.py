import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from core.notes_manager import NotesManager
from ui.web_tab import WebViewTab
from ui.search_tab import NotesSearchTab
from ui.editor_tab import TextEditorTab


class NoteNinja(QMainWindow):
    def __init__(self):
        super().__init__()
        self.notes_manager = NotesManager()
        self.init_ui()

    def init_ui(self):
        # Fancy title with feather pen
        self.setWindowTitle("🪶 NoteNinja — Smart Note Taking")
        self.setGeometry(100, 100, 1200, 800)

        # Set window icon (make sure assets/quill.png exists)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'assets', 'quill.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Tabs
        self.tab_widget = QTabWidget()
        self.web_tab = WebViewTab()
        self.search_tab = NotesSearchTab(self.notes_manager)
        self.editor_tab = TextEditorTab(self.notes_manager)

        self.tab_widget.addTab(self.web_tab, "🌐 Web Browser")
        self.tab_widget.addTab(self.search_tab, "🔍 Search Notes")
        self.tab_widget.addTab(self.editor_tab, "📝 Text Editor")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tab_widget)

    def on_tab_changed(self, index):
        if index == 1:
            self.search_tab.refresh_notes_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("NoteNinja")
    app.setApplicationVersion("1.0")

    window = NoteNinja()
    window.show()

    sys.exit(app.exec_())
