import mysql.connector
import json
import jwt
from unittest import result
from datetime import datetime, timedelta
from flask import make_response, send_file
from config.config import dbConfig


class user_model():
    def __init__(self):
        # db connection logic here
        try:
            self.con = mysql.connector.connect(
                host=dbConfig["host"],
                user=dbConfig["user"],
                password=dbConfig["password"],
                database=dbConfig["database"]
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
        self.cur.execute(f"INSERT INTO users (name, email, phone, role_id, password) VALUES ('{data["name"]}', '{data["email"]}','{data["phone"]}', '{data["role_id"]}','{data["password"]}')")
        return make_response({'message': 'User added successfully'}, 201)
    
    def user_add_multiple_model(self, data):
        for user in data:
            self.cur.execute(f"INSERT INTO users (name, email, phone, role_id, password) VALUES ('{user['name']}', '{user['email']}','{user['phone']}', '{user['role_id']}','{user['password']}')")
        return make_response({'message': 'Users added successfully'}, 201)
    
    def user_update_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data["name"]}', email='{data["email"]}', phone='{data["phone"]}', role_id='{data["role_id"]}', password='{data["password"]}' WHERE id={data['id']}")
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

    def user_pagination_model(self, limit, page):
        start = (page * limit) - limit
        print(start)
        qry = f'SELECT * FROM users LIMIT {start}, {limit}'
        self.cur.execute(qry)
        result = self.cur.fetchall()
        return make_response({'data':result, 'page': page, 'limit': limit}, 200)

    def user_upload_avatar_model(self, uid, file):
        user = self.cur.execute(f'SELECT * FROM users WHERE id={uid}')
        user = self.cur.fetchone()
        if(user is None):
            return make_response({'message': 'User not found'}, 404)
        else:
            uniqueFilename = str(datetime.now().timestamp()).replace('.', '')
            ext = file.filename.split('.')[-1]
            finalFilePath = f"uploads/{uniqueFilename}.{ext}"
            file.save(finalFilePath)
            self.cur.execute(f"UPDATE users SET avatar='{finalFilePath}' WHERE id={uid}")
            if self.cur.rowcount > 0:
                return make_response({'message': 'File uploaded successfully'}, 200)
            else:
                return make_response({'message': 'Nothing to update'}, 404)
    
    def user_get_avatar_model(self, uid):
        user = self.cur.execute(f'SELECT * FROM users WHERE id={uid}')
        user = self.cur.fetchone()
        if(user is None):
            return make_response({'message': 'User not found'}, 404)
        else:
            if user['avatar'] is not None and len(user['avatar']) > 0:
                return make_response(send_file(user['avatar']), 200)
            else:
                return make_response({'message': 'Avatar not found'}, 404)
            
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' AND password='{data['password']}'")
        result = self.cur.fetchone();
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload": result,
            "exp": exp_epoch_time
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return make_response({'token': token}, 200)

        