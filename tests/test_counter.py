from unittest import TestCase
from src.counter import app, status
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/test_counter')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/test_duplicate_counter')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/test_duplicate_counter')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        # Step 1: Create a counter
        create_result = self.client.post('/counters/update_test_counter')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Step 2: Check baseline counter value
        baseline_result = self.client.get('/counters/update_test_counter')
        baseline_value = baseline_result.json['update_test_counter']

        # Step 3: Update the counter
        update_result = self.client.put('/counters/update_test_counter')
        self.assertEqual(update_result.status_code, status.HTTP_200_OK)

        # Step 4: Check that the counter value is one more than the baseline
        updated_result = self.client.get('/counters/update_test_counter')
        updated_value = updated_result.json['update_test_counter']
        self.assertEqual(updated_value, baseline_value + 1)

    def test_read_a_counter(self):
        """It should read a counter"""
        # Step 1: Create a counter
        create_result = self.client.post('/counters/read_test_counter')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Step 2: Read the counter
        read_result = self.client.get('/counters/read_test_counter')
        self.assertEqual(read_result.status_code, status.HTTP_200_OK)
        self.assertIn('read_test_counter', read_result.json)

    def test_delete_counter(self):
        """It should delete a counter"""
        # Step 1: Create a counter
        create_result = self.client.post('/counters/delete_test_counter')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Step 2: Delete the counter
        delete_result = self.client.delete('/counters/delete_test_counter')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)

        # Step 3: Check that the counter no longer exists
        read_result = self.client.get('/counters/delete_test_counter')
        self.assertEqual(read_result.status_code, status.HTTP_404_NOT_FOUND)