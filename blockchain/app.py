import pathlib

from flask import Flask, render_template, request, jsonify

from blockchain import Blockchain
from document import Document

UPLOADS_PATH = pathlib.Path("uploads")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOADS_PATH)
blockchain = Blockchain()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def register_transaction():
    print(f"Register Transaction")
    files = (request.files.get("doc1", False), request.files.get("doc2", False))
    documents = []
    for f in files:
        if f.filename == "":
            print(f"Empty file")
            return '', 204
        filepath  = UPLOADS_PATH / f.filename
        f.save(str(filepath))
        documents.append(Document.document_from_file(filepath))

    for doc in documents:
        print(f"{doc.title}: {doc.body}")
    
    blockchain.add_transaction(*documents)
    similarity = blockchain.mine()
    return render_template("index.html", similarity=f"SIMILARITY - {int(100*similarity)}%")

@app.route("/getblockchain", methods=["GET"])
def send_blockchain():
    response = jsonify({"info": str(blockchain)})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    UPLOADS_PATH.mkdir(parents=True, exist_ok=True)
    app.run(debug=True)
