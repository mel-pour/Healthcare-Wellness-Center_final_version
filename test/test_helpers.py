import tempfile
from pathlib import Path

from data_access.text_file_storage import TextFileStorage


def make_storage(test):
    """Creates an empty data file in a temporary folder. The folder is deleted after the test."""
    folder = tempfile.TemporaryDirectory()
    test.addCleanup(folder.cleanup)
    storage = TextFileStorage(Path(folder.name) / "healthcare_data.txt")
    storage.save({"customers": [], "offerings": [], "appointments": [], "centers": []})
    return storage
