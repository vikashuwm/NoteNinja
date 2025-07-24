import os
import json
from datetime import datetime
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument


class NotesManager:
    """Handles saving, loading, deleting, and exporting notes."""

    def __init__(self):
        self.notes_dir = "notes"
        self.pdf_dir = "notes_pdf"
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure required directories exist."""
        os.makedirs(self.notes_dir, exist_ok=True)
        os.makedirs(self.pdf_dir, exist_ok=True)

    def save_note(self, title, content, existing_filename=None):
        """Save a note. If `existing_filename` is provided, it overwrites."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]

        filename = existing_filename or f"{timestamp}_{safe_title}.json"
        filepath = os.path.join(self.notes_dir, filename)

        note_data = {
            'title': title,
            'content': content,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'filename': filename
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(note_data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            print(f"[Error] Failed to save note: {e}")
            return None

    def get_all_notes(self):
        """Return all notes as a list of dictionaries sorted by date (newest first)."""
        notes = []
        try:
            for filename in os.listdir(self.notes_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.notes_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        note_data = json.load(f)
                        notes.append(note_data)
            notes.sort(key=lambda x: x['date'], reverse=True)
        except Exception as e:
            print(f"[Error] Failed to load notes: {e}")
        return notes

    def delete_note(self, filename):
        """Delete a note by filename."""
        try:
            filepath = os.path.join(self.notes_dir, filename)
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"[Error] Failed to delete note: {e}")
            return False

    def save_as_pdf(self, title, content):
        """Export note content to PDF."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]

            filename = f"{timestamp}_{safe_title}.pdf"
            filepath = os.path.join(self.pdf_dir, filename)

            document = QTextDocument()
            document.setPlainText(f"{title}\n\n{content}")

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filepath)

            document.print_(printer)
            return True
        except Exception as e:
            print(f"[Error] Failed to save PDF: {e}")
            return False
