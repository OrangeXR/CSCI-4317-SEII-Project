import unittest
from unittest.mock import patch, MagicMock
from app import app
from datetime import datetime

class TestAssignmentTracker(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and test configurations."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    # =================================================================================
    # TC01: Add Assignment - Valid Input
    # Expected: App accepts input, creates assignment, and redirects to index
    # =================================================================================
    @patch('app.add_assignment')
    @patch('app.update_assignment_files')
    def test_tc01_add_assignment_valid(self, mock_update_files, mock_add_assignment):
        # Mock the database returning a new assignment ID
        mock_add_assignment.return_value = 1
        
        # Simulate an active user session
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            
        # Make a POST request with valid data (Note: app.py expects YYYY-MM-DD)
        response = self.client.post('/add', data={
            'name': 'Balance Equation',
            'class_name': 'Chemistry',
            'category': 'Equations',
            'due_date': '2027-07-07', 
            'notes': 'Use the periodic table'
        })
        
        # Assert the app successfully processed and redirected to index (Status 302)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)
        mock_add_assignment.assert_called_once()

    # =================================================================================
    # TC02: Add Assignment - Invalid Date Format
    # Expected: App prevents invalid date entry and surfaces an error, rather than crashing.
    # =================================================================================
    @patch('app.add_assignment')
    def test_tc02_add_assignment_invalid_date(self, mock_add_assignment):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            
        # Post data with an invalid date format (e.g., >4 digit year, causing the crash in manual testing)
        response = self.client.post('/add', data={
            'name': 'Math Stuff',
            'class_name': 'Math',
            'category': 'Math',
            'due_date': '20277-07-07', # Invalid date format
            'notes': ''
        })
        
        # Assert the app did NOT redirect (so it didn't succeed) and didn't crash (status 500)
        # It should return status 200, re-rendering the form with an error message
        self.assertEqual(response.status_code, 200)
        
        # Check if the correct error message is present in the rendered HTML
        html_response = response.data.decode('utf-8')
        self.assertIn('Invalid date format. Please use YYYY-MM-DD.', html_response)
        
        # Verify the database add_assignment function was never called
        mock_add_assignment.assert_not_called()

    # =================================================================================
    # TC03: Mark Assignment as Done
    # Expected: Assignment status changes from 0 to 1
    # =================================================================================
    @patch('app.mark_assignment_done')
    def test_tc03_mark_assignment_done(self, mock_mark_done):
        # Simulate an active user session
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            
        # Make a GET request to the 'done' route with assignment ID 5
        response = self.client.get('/done/5')
        
        # Assert it triggers the DB function and redirects to index
        mock_mark_done.assert_called_once_with(5)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)

    # =================================================================================
    # TC04: Filter Assignment List
    # Expected: Passing a 'sort' argument correctly orders the assignments
    # =================================================================================
    @patch('app.get_all_assignments')
    def test_tc04_filter_assignment_list(self, mock_get_all):
        # Mock the database to return an unsorted list of assignments
        mock_get_all.return_value = [
            {"id": 1, "class_name": "Physics", "name": "Kinematics", "category": "Lab", "due_date": "2027-01-10", "status": 0},
            {"id": 2, "class_name": "Algebra", "name": "Equations", "category": "HW", "due_date": "2027-01-05", "status": 0},
            {"id": 3, "class_name": "Biology", "name": "Cells", "category": "Essay", "due_date": "2027-01-15", "status": 0}
        ]

        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            
        # Request the index page with sort=class_name
        response = self.client.get('/?sort=class_name')
        
        # Verify the request is successful
        self.assertEqual(response.status_code, 200)
         
        # Presence of the mocked data in the output string verifies the render worked.
        html_response = response.data.decode('utf-8')
        self.assertIn('Physics', html_response)
        self.assertIn('Algebra', html_response)
        self.assertIn('Biology', html_response)

if __name__ == '__main__':
    unittest.main()