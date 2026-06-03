from flask import Flask

from controllers import blueprints

app = Flask(__name__)

for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/')
def welcome():
    return 'Welcome to the Flask app!'

@app.route('/home')
def home():
    return 'Welcome to the home page!'

if __name__ == '__main__':
    app.run(debug=True)