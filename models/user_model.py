from unittest import result

import mysql.connector
import json
from flask import make_response

class user_model():
    def __init__(self):
        # db connection logic here
        try:
            self.con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='flask_learning'
            )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Database connection successful')
        except:
            print('Error while connecting to database')

    def user_getall_model(self):
        # query execution logic here
        self.cur.execute('SELECT * FROM users')
        result = self.cur.fetchall()
        if len(result) > 0:
            return make_response({'data':result}, 200)
        else:
            return make_response({'message': 'No users found'}, 204)

    def user_get_model(self, id):
        self.cur.execute(f'SELECT * FROM users WHERE id={id}')
        result = self.cur.fetchone()
        if result is not None and len(result) > 0:
            return make_response({'data':result}, 200)
        else:
            return make_response({'message': 'No users found'}, 204)

    def user_add_model(self, data):
        self.cur.execute(f"INSERT INTO users (name, email, phone, role, password) VALUES ('{data["name"]}', '{data["email"]}','{data["phone"]}', '{data["role"]}','{data["password"]}')")
        return make_response({'message': 'User added successfully'}, 201)
    
    def user_update_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data["name"]}', email='{data["email"]}', phone='{data["phone"]}', role='{data["role"]}', password='{data["password"]}' WHERE id={data['id']}")
        if self.cur.rowcount > 0:
            return make_response({'message': 'User updated successfully'}, 200)
        else:
            return make_response({'message': 'User not found'}, 404)

    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount > 0:
            return make_response({'message': 'User deleted successfully'}, 200)
        else:
            return make_response({'message': 'User not found'}, 404)

    def user_patch_model(self, id, data):
        qry = 'UPDATE users SET '
        print(data)
        for key in data:
            print(data[key])
            qry += f"{key}='{data[key]}', "
        qry = qry[:-2] + f" WHERE id={id}"
        
        self.cur.execute(qry)
        if self.cur.rowcount > 0:
            return make_response({'message': 'User updated successfully'}, 200)
        else:
            return make_response({'message': 'User not found'}, 404)

        