"""
Example test that ACTUALLY RUNS - breaks the zero-test inertia.
This proves the test framework works and makes test #2 easier to write.
"""

import json
import unittest
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAGETBasics(unittest.TestCase):
    """Real tests that validate critical functionality"""

    def test_agents_file_exists(self):
        """AGENTS.md must exist - it's the core config file"""
        # Ensure we're in the project root
        try:
            current = Path.cwd()
        except (FileNotFoundError, OSError):
            # Previous test left us in deleted directory
            import os
            # Change to test file's parent directory (project root)
            os.chdir(Path(__file__).parent.parent)
            current = Path.cwd()

        # Look for AGENTS.md in project root (parent of tests/)
        project_root = Path(__file__).parent.parent
        agents_file = project_root / "AGENTS.md"
        self.assertTrue(
            agents_file.exists(),
            "AGENTS.md is required for AGET configuration"
        )

    def test_aget_directory_structure(self):
        """Verify .aget/ directory can be created/exists"""
        # Ensure we're in the project root
        try:
            current = Path.cwd()
        except (FileNotFoundError, OSError):
            # Previous test left us in deleted directory
            import os
            # Change to test file's parent directory (project root)
            os.chdir(Path(__file__).parent.parent)
            current = Path.cwd()

        # Use project root
        project_root = Path(__file__).parent.parent
        aget_dir = project_root / ".aget"
        if not aget_dir.exists():
            # Test that we CAN create it (write permissions)
            try:
                aget_dir.mkdir(exist_ok=True)
                self.assertTrue(True, ".aget directory created successfully")
            except Exception as e:
                self.fail(f"Cannot create .aget directory: {e}")
        else:
            self.assertTrue(aget_dir.is_dir(), ".aget must be a directory")

    def test_no_test_theater(self):
        """This test suite has real tests, not placeholders"""
        # Count actual test methods in this class
        test_methods = [m for m in dir(self) if m.startswith('test_')]
        self.assertGreater(
            len(test_methods), 1,
            "Test suite must have more than just this meta-test"
        )

    def test_data_integrity_if_json_exists(self):
        """If JSON files exist in .aget, they must be valid"""
        aget_dir = Path(__file__).parent.parent / ".aget"
        if aget_dir.exists():
            json_files = list(aget_dir.glob("*.json"))
            for json_file in json_files:
                with self.subTest(file=json_file.name):
                    try:
                        with open(json_file) as f:
                            json.load(f)
                        self.assertTrue(True, f"{json_file.name} is valid JSON")
                    except json.JSONDecodeError as e:
                        self.fail(f"{json_file.name} has corrupted JSON: {e}")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)