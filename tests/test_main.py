import unittest
import os
import tempfile
from gcont.main import detect_project_type, gather_code_files, get_language_by_extension

class TestGcont(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_root = self.test_dir.name

        # Create files and directories to simulate different project types
        os.makedirs(os.path.join(self.test_root, 'node_modules'))
        os.makedirs(os.path.join(self.test_root, 'components'))
        os.makedirs(os.path.join(self.test_root, 'components', 'utils'))
        os.makedirs(os.path.join(self.test_root, 'venv'))
        os.makedirs(os.path.join(self.test_root, '.git'))

        # Create some files
        with open(os.path.join(self.test_root, 'manage.py'), 'w') as f:
            f.write("# Django manage file")
        with open(os.path.join(self.test_root, 'requirements.txt'), 'w') as f:
            f.write("Django==3.2")
        with open(os.path.join(self.test_root, 'components', 'index.js'), 'w') as f:
            f.write("// React component")
        with open(os.path.join(self.test_root, 'components', 'utils', 'helper.js'), 'w') as f:
            f.write("// Helper function")
        with open(os.path.join(self.test_root, 'node_modules', 'module.js'), 'w') as f:
            f.write("// Node module")
        with open(os.path.join(self.test_root, 'venv', 'script.py'), 'w') as f:
            f.write("# Python virtual environment script")
        with open(os.path.join(self.test_root, '.git', 'config'), 'w') as f:
            f.write("# Git config")

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_detect_project_type(self):
        """Test project type detection."""
        self.assertEqual(detect_project_type(self.test_root), "django")
        
        # Remove Django-specific files and add Node.js files
        os.remove(os.path.join(self.test_root, 'manage.py'))
        os.remove(os.path.join(self.test_root, 'requirements.txt'))
        with open(os.path.join(self.test_root, 'package.json'), 'w') as f:
            f.write("{ }")

        self.assertEqual(detect_project_type(self.test_root), "nodejs")

    def test_gather_code_files_with_exclusions(self):
        """Test gathering files with exclusion patterns."""
        include_patterns = ["*.js", "*.py"]
        # Adding explicit pattern to exclude 'manage.py' if it shouldn't be included
        exclude_patterns = ["node_modules/*", ".git/*", "venv/*", "manage.py"]

        gathered_files = gather_code_files([self.test_root], include_patterns, exclude_patterns)
        expected_files = [
            os.path.join(self.test_root, 'components', 'index.js'),
            os.path.join(self.test_root, 'components', 'utils', 'helper.js')
        ]
        self.assertCountEqual(gathered_files, expected_files)


    def test_gather_code_files_with_inclusions(self):
        """Test gathering files with specific inclusion patterns."""
        include_patterns = ["*.js"]
        exclude_patterns = []
        
        gathered_files = gather_code_files([self.test_root], include_patterns, exclude_patterns)
        expected_files = [
            os.path.join(self.test_root, 'components', 'index.js'),
            os.path.join(self.test_root, 'components', 'utils', 'helper.js'),
            os.path.join(self.test_root, 'node_modules', 'module.js')
        ]
        self.assertCountEqual(gathered_files, expected_files)

    def test_get_language_by_extension(self):
        """Test language detection based on file extensions."""
        self.assertEqual(get_language_by_extension("script.py"), "python")
        self.assertEqual(get_language_by_extension("index.js"), "javascript")
        self.assertEqual(get_language_by_extension("styles.css"), "css")
        self.assertEqual(get_language_by_extension("unknown.ext"), "")

if __name__ == "__main__":
    unittest.main()
