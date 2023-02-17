from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pymongo import MongoClient

class EmployeeAPI:
    def __init__(self, app, client):
        self.app = app
        self.client = client
        self.db = client["employee_db"]
        self.col = self.db["employees"]
        
        # permettre l'accès depuis n'importe quelle origine
        CORS(self.app)
        
        # définir les routes de l'API
        self.app.add_url_rule('/api/v1/employees', view_func=self.get_employees, methods=['GET'])
        self.app.add_url_rule('/api/v1/employees', view_func=self.add_employee, methods=['POST'])
        self.app.add_url_rule('/api/v1/employees/<int:employee_id>', view_func=self.get_employee, methods=['GET'])
        self.app.add_url_rule('/api/v1/employees/<int:employee_id>', view_func=self.delete_employee, methods=['DELETE'])
        self.app.add_url_rule('/api/v1/employees/<int:employee_id>', view_func=self.update_employee, methods=['PUT'])
    
    def get_employees(self):
        cursor = self.col.find({}, {'_id': 0})
        liste = [i for i in cursor]
        response = jsonify(liste)
        return make_response(response, 200)
    
    def add_employee(self):
        data = request.get_json()
        cursor = self.col.find({}, {'_id': 0})
        liste = [i for i in cursor]            
        try:
            data['id'] = liste[-1]['id'] + 1  
        except:
            data['id'] = 1
        self.col.insert_one(data).inserted_id
        del data['_id'] # Permet de serialiser le JSON par le suite
        response = jsonify(data)
        return make_response(response, 200)
    
    def get_employee(self, employee_id):
        cursor = self.col.find({'id': employee_id}, {'_id': 0})
        employee = cursor.next()
        response = jsonify(employee)
        return make_response(response, 200)
    
    def delete_employee(self, employee_id):
        cursor = self.col.find({'id': employee_id}, {'_id': 0})
        employee = cursor.next()
        if employee:
            self.col.delete_one({'id': employee_id})
            response = jsonify()
            return make_response(response, 204)
        else:
            error = {'error': f'Employee with id {employee_id} not found'}
            response = jsonify(error)
            return make_response(response, 404)
    
    def update_employee(self, employee_id):
        employee = self.col.find_one({'id': employee_id})
        if not employee:
            error = {'error': f'Employee with id {employee_id} not found'}
            response = jsonify(error)
            return make_response(response, 404)
        else:
            data = request.get_json()
            self.col.update_one(
                {'id': employee_id},    
                {
                    "$set": {
                        'firstName': data.get('firstName', employee['firstName']),
                        'lastName': data.get('lastName', employee['lastName']),
                        'emailId': data.get('emailId', employee['emailId'])
                    }
                }
            )
            response = jsonify()
            return make_response(response, 204)

app = Flask('__name__')
client = MongoClient('mongodb://root:example@localhost:27017/')
api = EmployeeAPI(app, client)

if __name__ == '__main__':
    app.run(debug=True)