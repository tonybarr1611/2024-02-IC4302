import csv
import unittest
from app import readCSVFile
from unittest.mock import Mock

class TestReadCSVFile(unittest.TestCase):
    def test_readCSVFile_with_data(self):
        mock_blob = Mock()
        csv_content = "Name,Genres,Songs,Popularity,Link\nArtist1,Pop,Song1,90,link1\nArtist2,Rock,Song2,80,link2"
        mock_blob.download_as_text.return_value = csv_content

        result = readCSVFile(mock_blob)

        expected = [
            ["Artist1", "Pop", "Song1", "90", "link1"],
            ["Artist2", "Rock", "Song2", "80", "link2"]
        ]

        self.assertEqual(result, expected)

    def test_readCSVFile_empty_file(self):
        mock_blob = Mock()
        mock_blob.download_as_text.return_value = "Name,Genres,Songs,Popularity,Link\n"

        result = readCSVFile(mock_blob)

        self.assertEqual(result, [])

    def test_readCSVFile_with_incomplete_data(self):
        mock_blob = Mock()
        csv_content = "Name,Genres,Songs,Popularity,Link\nArtist1,Pop,Song1,90\nArtist2,Rock,Song2"
        mock_blob.download_as_text.return_value = csv_content

        result = readCSVFile(mock_blob)

        expected = [
            ["Artist1", "Pop", "Song1", "90"],
            ["Artist2", "Rock", "Song2"]
        ]

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
