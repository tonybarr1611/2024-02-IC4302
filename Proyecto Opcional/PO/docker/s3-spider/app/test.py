import re
import unittest

def extract_dois(text):
    doi_pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b'

    potential_dois = re.findall(doi_pattern, text, flags=re.IGNORECASE)
    
    valid_dois = list(set(potential_dois))  # Use set to remove duplicates

    valid_dois.sort()

    return valid_dois

def create_jobs(data, job_size):
    dois = extract_dois(data)
    
    jobs = [dois[i:i + job_size] for i in range(0, len(dois), job_size)]
    
    return jobs

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

if __name__ == "__main__":
    unittest.main()