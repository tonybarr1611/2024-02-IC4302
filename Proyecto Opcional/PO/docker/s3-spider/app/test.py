import unittest

class TestDownloaderFunctions(unittest.TestCase):
    def test_extract_dois(self):
        sample_text = "Here are some DOIs: 10.1000/182, 10.1001/876446."
        expected_dois = ['10.1000/182', '10.1001/876446']
        result = extract_dois(sample_text)
        result.sort()
        self.assertEqual(result, expected_dois)

    def test_create_jobs(self):
        dois = ['10.1000/182', '10.1001/757743', '10.1002/24343']
        job_size = 2
        expected_jobs = [['10.1000/182', '10.1001/757743'], ['10.1002/24343']]
        
        result = create_jobs(' '.join(dois), job_size)

        self.assertEqual(result, expected_jobs)

    