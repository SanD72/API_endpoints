import unittest
from flask import Flask
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_create_task_success(self):
        response = self.app.post('/tasks', json={"title": "Test Task", "description": "Test Description", "completed": False})
        self.assertEqual(response.status_code, 201)

    def test_create_task_unauthorized(self):
        response = self.app.post('/tasks', json={"title": "Test Task", "description": "Test Description", "completed": False}, headers={"Authorization": "invalid_api_key"})
        self.assertEqual(response.status_code, 401)
    
    def test_get_all_tasks_success(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_get_task_success(self):
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)

    def test_get_task_not_found(self):
        response = self.app.get('/tasks/999')
        self.assertEqual(response.status_code, 404)

    def test_update_task_success(self):
        response = self.app.put('/tasks/1', json={"title": "Updated Task", "description": "Updated Description", "completed": True})
        self.assertEqual(response.status_code, 200)

    def test_update_task_not_found(self):
        response = self.app.put('/tasks/999', json={"title": "Updated Task", "description": "Updated Description", "completed": True})
        self.assertEqual(response.status_code, 404)
    
    def test_delete_task_success(self):
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_task_not_found(self):
        response = self.app.delete('/tasks/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()