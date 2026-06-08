import mysql.connector
import re
import jwt
from functools import wraps
from flask import make_response, send_file ,request, json
from config.config import dbConfig

class auth_model():
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

    def token_auth(self, endpoint =''):
        def innerFunc1(func):
            @wraps(func)
            def innerFunc2(*args):
                endpoint = request.url_rule
                print(endpoint)
                bearerToken = request.headers.get('Authorization')
                if re.match("^Bearer *([^ ]+) *$", bearerToken, flags=0):
                    token = bearerToken.split(' ')[1]
                    try:
                        jwtDecoded = jwt.decode(token, 'secret', algorithms='HS256')
                        role_id = jwtDecoded['payload']['role_id']
                        self.cur.execute(f"SELECT roles FROM flask_learning.accessibility_view WHERE endpoint = '{endpoint}'")
                        result = self.cur.fetchall()
                        if result is not None and len(result) > 0:
                            allowed_roles = json.loads(result[0]['roles'])
                            if role_id in allowed_roles:
                                return func(*args)  
                            else:
                                return {'error': 'Unauthorized access'}, 403
                        else:
                            return {'error': 'Endpoint not found'}, 404
                    except jwt.ExpiredSignatureError:
                        return {'error': 'Expired token'}, 401
                    except jwt.InvalidTokenError:
                        return {'error': 'Invalid token'}, 401
                else:
                    return {'error': 'Invalid or missing token'}, 401
            return innerFunc2
        return innerFunc1
