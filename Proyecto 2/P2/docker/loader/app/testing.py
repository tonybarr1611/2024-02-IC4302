import unittest
from unittest.mock import Mock
import pandas as pd
from io import StringIO
from app import readCSVFile  # replace 'your_module' with the actual name of your module

class TestReadCSVFile(unittest.TestCase):

    def test_readCSVFile_with_standard_data(self):
        # Mock blob with standard CSV content
        mock_blob = Mock()
        csv_content = "Name,Genres,Songs,Popularity,Link\nArtist1,Pop,Song1,90,link1\nArtist2,Rock,Song2,80,link2"
        mock_blob.download_as_text.return_value = csv_content
        mock_blob.name = 'artists-data.csv'  # Test as artists data

        result = readCSVFile(mock_blob)

        expected = [
            ['Artist1', 'Pop', 'Song1', 90, 'link1'],
            ['Artist2', 'Rock', 'Song2', 80, 'link2']
        ]

        self.assertEqual(result, expected)

    def test_readCSVFile_with_lyrics(self):
        # Mock blob with Lyric content (different CSV name triggers Lyric column handling)
        mock_blob = Mock()
        csv_content = "ArtistLink,Name,Link,Lyric,Language\nlink1,Song1,link1,'This is the first line\\nsecond line',EN\nlink2,Song2,link2,'Another lyric',EN"
        mock_blob.download_as_text.return_value = csv_content
        mock_blob.name = 'songs-data.csv'  # Not artists-data.csv, so Lyric column should be altered

        result = readCSVFile(mock_blob)

        expected = [
            ['link1', 'Song1', 'link1', "'This is the first line\\nsecond line'", 'EN'],
            ['link2', 'Song2', 'link2', "'Another lyric'", 'EN']
        ]

        self.assertEqual(result, expected)

    def test_readCSVFile_with_incomplete_data(self):
        # Mock blob with incomplete rows
        mock_blob = Mock()
        csv_content = "Name,Genres,Songs,Popularity,Link\nArtist1,Pop,,,\nArtist2,Rock,Song2,80,link2"
        mock_blob.download_as_text.return_value = csv_content
        mock_blob.name = 'artists-data.csv'

        result = readCSVFile(mock_blob)

        # Incomplete row should be removed
        expected = [
            ["Artist2", "Rock", "Song2", "80", "link2"]
        ]

        self.assertEqual(result, expected)

    def test_readCSVFile_with_empty_file(self):
        # Mock blob with header only
        mock_blob = Mock()
        csv_content = "Name,Genres,Songs,Popularity,Link\n"
        mock_blob.download_as_text.return_value = csv_content
        mock_blob.name = 'artists-data.csv'

        result = readCSVFile(mock_blob)

        # Expected to be empty since there's no data
        self.assertEqual(result, [])

    def test_readCSVFile_with_exception(self):
        # Mock blob that raises an exception during download
        mock_blob = Mock()
        mock_blob.download_as_text.side_effect = Exception("Download failed")
        mock_blob.name = 'artists-data.csv'

        result = readCSVFile(mock_blob)

        # Expected to handle exception gracefully and return an empty list
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
