from flask import Flask, request, jsonify
from pathlib import Path
from model import calc_similarity

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello():
    s1 = request.form['sentence1']
    s2 = request.form['sentence2']
    print(s1, s2)
    similarity = calc_similarity(s1, s2)
    similarity = str(int(100*similarity)) + '%'
    response = jsonify({'similarity': similarity})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)