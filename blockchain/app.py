from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def hello():
    s1 = request.form['sentence1']
    s2 = request.form['sentence2']
    print(s1, s2)
    similarity = 0.7 # PLACEHOLDER
    similarity = str(int(100*similarity)) + '%'
    response = jsonify({'similarity': similarity})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)
