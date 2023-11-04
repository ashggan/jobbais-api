from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    data = {
        'message': 'Hello, World!'
    }
    return jsonify(data)

@app.route('/about')
def about():
    return 'About'