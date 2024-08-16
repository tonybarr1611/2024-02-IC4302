import os
import unittest
from unittest.mock import patch, MagicMock
from app import execute_query, get_doi_information, save_json

XPATH=os.getenv('XPATH')
API = 'https://api.crossref.org/works/'

class TestDownloaderFunctions(unittest.TestCase):
    @patch('mariadb.ConnectionPool')
    def test_execute_query(self, MockConnectionPool):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_cursor.fetchall.return_value = [('mock_result',)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        MockConnectionPool.return_value.get_connection.return_value = mock_conn

        result = execute_query("SELECT * FROM mock_table WHERE id = %s", [1])
        self.assertEqual(result, [('mock_result',)])

    @patch('requests.get')
    def test_get_doi_information(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'mock_key': 'mock_value'}
        mock_get.return_value = mock_response

        result = get_doi_information('mock_doi')
        self.assertEqual(result, {'mock_key': 'mock_value'})

    @patch('builtins.open', unittest.mock.mock_open())
    def test_save_json(self):
        data = {'mock_key': 'mock_value'}
        result = save_json('mock_name', data)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()