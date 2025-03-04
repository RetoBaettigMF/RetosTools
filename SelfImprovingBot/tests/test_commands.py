import unittest
import os
import tempfile
from utils.commands import Commands

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
        
    def test_file_operations(self):
        """Test basic file operations."""
        # Test writing to a file
        test_content = "Hello, world!"
        Commands.write_file(self.test_file, test_content)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Test reading from a file
        read_content = Commands.read_file(self.test_file)
        self.assertEqual(read_content, test_content)
        
        # Test appending to a file
        append_content = "\nAppended text"
        Commands.append_file(self.test_file, append_content)
        read_content = Commands.read_file(self.test_file)
        self.assertEqual(read_content, test_content + append_content)
        
        # Test listing files
        files = Commands.list_files(self.test_dir)
        self.assertIn("test_file.txt", files)
        
    def test_directory_operations(self):
        """Test directory operations."""
        new_dir = os.path.join(self.test_dir, "new_dir")
        Commands.create_directory(new_dir)
        self.assertTrue(os.path.exists(new_dir))
        self.assertTrue(os.path.isdir(new_dir))

if __name__ == "__main__":
    unittest.main()