from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'

app.config['MONGO_dbname'] = 'users'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'

mongo = PyMongo(app)

import jwt
import datetime

# Secret key for encoding and decoding the token
SECRET_KEY = 'this is my secret key'

# Generate a token with a 30-minute expiration
def generate_token():
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(minutes=30)
    payload = {
        'exp': expiration_time,
        'iat': current_time
        # You can add more data to the payload as needed
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Decode and verify a token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has expired."
    except jwt.DecodeError:
        return "Token is invalid."
    
# Example of generating and verifying a token
token = generate_token()
print("Generated Token:", token)

decoded_payload = verify_token(token)
print("Decoded Payload:", decoded_payload)




if __name__ == "__main__":
    app.run(debug=True)
    app.run()