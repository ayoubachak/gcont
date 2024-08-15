import unittest
import os
from gcont.main import detect_project_type, gather_code_files, get_language_by_extension

class TestGcont(unittest.TestCase):

    def setUp(self):
        """Set up test directories and files."""
        self.root_dir = 'test_gather'
        os.makedirs(self.root_dir, exist_ok=True)
        
        # Create some test files
        with open(os.path.join(self.root_dir, 'example.py'), 'w') as f:
            f.write('print("Hello World")')
        
        with open(os.path.join(self.root_dir, 'example.txt'), 'w') as f:
            f.write('This is a text file.')
        
        os.makedirs(os.path.join(self.root_dir, 'venv'), exist_ok=True)
        with open(os.path.join(self.root_dir, 'venv', 'dummy.py'), 'w') as f:
            f.write('print("This should be excluded")')

    def tearDown(self):
        """Clean up the test directories and files."""
        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.root_dir)

    def test_detect_project_type_django(self):
        root_dir = 'test_project_django'
        os.makedirs(root_dir, exist_ok=True)
        with open(os.path.join(root_dir, 'manage.py'), 'w') as f:
            f.write('print("Django project")')
        with open(os.path.join(root_dir, 'requirements.txt'), 'w') as f:
            f.write('Django')
        self.assertEqual(detect_project_type(root_dir), "django")
        os.remove(os.path.join(root_dir, 'manage.py'))
        os.remove(os.path.join(root_dir, 'requirements.txt'))
        os.rmdir(root_dir)

    def test_detect_project_type_flask(self):
        root_dir = 'test_project_flask'
        os.makedirs(root_dir, exist_ok=True)
        with open(os.path.join(root_dir, 'app.py'), 'w') as f:
            f.write('print("Flask project")')
        with open(os.path.join(root_dir, 'requirements.txt'), 'w') as f:
            f.write('Flask')
        self.assertEqual(detect_project_type(root_dir), "flask")
        os.remove(os.path.join(root_dir, 'app.py'))
        os.remove(os.path.join(root_dir, 'requirements.txt'))
        os.rmdir(root_dir)

    def test_get_language_by_extension(self):
        self.assertEqual(get_language_by_extension('example.py'), 'python')
        self.assertEqual(get_language_by_extension('example.js'), 'javascript')
        self.assertEqual(get_language_by_extension('example.txt'), '')

    def test_gather_code_files_include(self):
        """Test gathering files with include patterns."""
        gathered_files = gather_code_files([self.root_dir], ['*.py'], [])
        self.assertEqual(len(gathered_files), 2)  # Both 'example.py' and 'venv/dummy.py' should be included
        self.assertTrue('example.py' in gathered_files[0])
        self.assertTrue('dummy.py' in gathered_files[1])

    def test_gather_code_files_exclude(self):
        """Test gathering files with exclude patterns."""
        gathered_files = gather_code_files([self.root_dir], ['*.py'], [os.path.join(self.root_dir, 'venv/*')])
        self.assertEqual(len(gathered_files), 1)  # Only 'example.py' should be included
        self.assertTrue('example.py' in gathered_files[0])
        self.assertFalse(any('dummy.py' in file for file in gathered_files))


if __name__ == '__main__':
    unittest.main()
