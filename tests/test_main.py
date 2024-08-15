import unittest
import os
from gcont.main import detect_project_type, gather_code_files, get_language_by_extension

class TestGcont(unittest.TestCase):

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

    def test_gather_code_files(self):
        root_dir = 'test_gather'
        os.makedirs(root_dir, exist_ok=True)
        with open(os.path.join(root_dir, 'example.py'), 'w') as f:
            f.write('print("Hello World")')
        gathered_files = gather_code_files([root_dir], ['*.py'], [])
        self.assertEqual(len(gathered_files), 1)
        self.assertTrue('example.py' in gathered_files[0])
        os.remove(os.path.join(root_dir, 'example.py'))
        os.rmdir(root_dir)

if __name__ == '__main__':
    unittest.main()
