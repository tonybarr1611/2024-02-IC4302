import os
import unittest
import hashlib
import json
import requests
from unittest.mock import patch, MagicMock

XPATH='./'
API = 'https://api.crossref.org/works/'

def get_doi_information(doi_id):
    try:
        response = requests.get(API + doi_id)
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def save_json(name, data):
    md5_doi = hashlib.md5(name.encode()).hexdigest()
    filename = f"MD5({md5_doi}).json"
    filepath = os.path.join(XPATH, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    return True

class TestDownloaderFunctions(unittest.TestCase):
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