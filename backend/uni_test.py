from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import unittest

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://root:example@mongo:27017/')
db = client["db"]
col = db["employees"]


class EmployeeAPI:
    def __init__(self):
        pass

@staticmethod
@app.route('/api/v1/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        employees_list = []
        try:
            cursor = col.find({}, {'_id': 0})
            for employee in cursor:
                employees_list.append(employee)
        except ValueError as err:
            return jsonify({'message': 'Erreur : {}'.format(str(err))}), 500
        return jsonify(employees_list), 200

    if request.method == 'POST':
        data = request.get_json()
        cursor = col.find({}, {'_id': 0})
        try:
            employee_id = max([employee['id'] for employee in cursor]) + 1
        except ValueError:
            employee_id = 1
        data['id'] = employee_id
        col.insert_one(data)
        return jsonify(data), 200



    @staticmethod
    @app.route('/api/v1/employees/<int:employee_id>', methods=['GET', 'DELETE', 'PUT'])
    def employee(employee_id):
        if request.method == 'GET':
            employee = col.find_one({'id': employee_id}, {'_id': 0})
            if employee:
                return jsonify(employee), 200
            else:
                return jsonify({'message': 'Employee not found'}), 404

        if request.method == 'DELETE':
            result = col.delete_one({'id': employee_id})
            if result.deleted_count == 1:
                return jsonify({'message': 'Employee deleted successfully'}), 200
            else:
                return jsonify({'message': 'Employee not found'}), 404

        if request.method == 'PUT':
            data = request.get_json()
            result = col.update_one({'id': employee_id}, {'$set': data})
            if result.modified_count == 1:
                return jsonify({'message': 'Employee updated successfully'}), 200
            else:
                return jsonify({'message': 'Employee not found'}), 404

class EmployeeAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.apihandler = EmployeeAPI()
    
    def test_get_method(self):
        response = self.app.get('/api/v1/employees')
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        response = self.app.post('/api/v1/employees', data= "{'name': 'ABC', 'address': '123 main st'}")
        self.assertEqual(response.status_code, 200)

    def test_put_method(self):
        self.app.post('/api/v1/employees', data= "{'name': 'ABC', 'address': '123 main st'}")
        response = self.app.put('/api/v1/employees/1', data="{'name': 'XYZ', 'address': '456 main st'}")
        self.assertEqual(response.status_code, 200)


    def test_delete_method(self):
        self.app.post('/api/v1/employees', data = "{'name': 'ABC', 'address': '123 main st'}")
        response = self.app.delete('/api/v1/employees/1')
        self.assertEqual(response.status_code, 200) 
