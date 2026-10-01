"""Le contenu doit rester identique avec le décodage Windows historique."""
import importlib
from pathlib import Path
from app import content

def test_content_reads_utf8_even_with_windows_default(monkeypatch):
    original=Path.read_text
    def windows_read(path,encoding=None,errors=None):
        return original(path,encoding=encoding or 'cp1252',errors=errors)
    expected=content.read('questions')
    monkeypatch.setattr(Path,'read_text',windows_read)
    assert content.read('questions')==expected
    assert content.read('sources')[0]['filename']
