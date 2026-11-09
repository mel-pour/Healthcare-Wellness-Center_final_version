import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def source_of(folder):
    return {path.name: path.read_text(encoding="utf-8") for path in (PROJECT / folder).glob("*.py")}


class TestArchitecture(unittest.TestCase):
    def test_models_use_properties_not_get_and_set_methods(self):
        for name, source in source_of("models").items():
            self.assertNotIn("def get_", source, name)
            self.assertNotIn("def set_", source, name)
            self.assertNotIn("re.fullmatch", source, name)

    def test_only_controllers_catch_errors(self):
        for folder in ("models", "views", "services", "data_access", "validation"):
            for name, source in source_of(folder).items():
                self.assertNotIn("try:", source, f"{folder}/{name}")

    def test_only_text_file_storage_opens_files(self):
        for folder in ("models", "views", "controllers", "services", "data_access", "validation"):
            for name, source in source_of(folder).items():
                if name != "text_file_storage.py":
                    self.assertNotIn("open(", source, f"{folder}/{name}")

    def test_each_layer_only_imports_the_layer_below(self):
        not_allowed = {
            "controllers": ("from data_access", "from views"),
            "services": ("from services", "from controllers", "from views"),
            "data_access": ("from services", "from controllers", "from views", "from data_access"),
        }
        for folder, imports in not_allowed.items():
            for name, source in source_of(folder).items():
                for line in imports:
                    self.assertNotIn(line, source, f"{folder}/{name}")


if __name__ == "__main__":
    unittest.main()
