from flask import Flask, render_template, request, jsonify

from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def register_transaction():
    first_string = request.form["sentence1"]
    second_string = request.form["sentence2"]

    blockchain.add_transaction(first_string, second_string)
    similarity = blockchain.mine()
    
    similarity = f"{int(100*similarity)}%"
    response = jsonify({"similarity": similarity})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/getblockchain", methods=["GET"])
def send_blockchain():
    response = jsonify({"info": str(blockchain)})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)
