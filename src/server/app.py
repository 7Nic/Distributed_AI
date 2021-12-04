from flask import Flask, render_template, jsonify
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    # return "Hello Nickson"
    response = jsonify({'similarity': 'Similarity here'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

