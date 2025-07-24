import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

class NoteNinja(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoteNinja")
        self.setGeometry(100, 100, 600, 400)
        self.notes = []

        self.editor = QTextEdit()
        self.save_button = QPushButton("Save Note")
        self.save_button.clicked.connect(self.save_note)

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_note(self):
        text = self.editor.toPlainText()
        self.notes.append(text)
        print("Note saved:", text)
        self.editor.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteNinja()
    window.show()
    sys.exit(app.exec_())
