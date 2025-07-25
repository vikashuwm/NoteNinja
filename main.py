import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from ui.web_tab import WebViewTab
from ui.search_tab import NotesSearchTab
from ui.editor_tab import TextEditorTab


class NoteNinja(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🪶 NoteNinja")
        self.setGeometry(100, 100, 1200, 800)

        # Set window icon if available
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'assets', 'quill.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Central layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Tabs
        self.tab_widget = QTabWidget()
        self.web_tab = WebViewTab()
        self.search_tab = NotesSearchTab()
        self.editor_tab = TextEditorTab()

        self.tab_widget.addTab(self.search_tab, "🔍 Search Notes")
        self.tab_widget.addTab(self.editor_tab, "📝 Text Editor")
        self.tab_widget.addTab(self.web_tab, "🌐 Web Browser")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tab_widget)

    def on_tab_changed(self, index):
        if index == 1:
            print("Switched to Search Notes tab")
            # Optional: refresh dummy list if needed
            if hasattr(self.search_tab, 'populate_dummy_notes'):
                self.search_tab.populate_dummy_notes()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("NoteNinja")
    app.setApplicationVersion("1.0")

    window = NoteNinja()
    window.show()

    sys.exit(app.exec_())
