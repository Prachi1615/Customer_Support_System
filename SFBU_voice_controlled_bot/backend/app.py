# Content of app.py
from flask import Flask, request, jsonify
from utils import load_db

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app,origins='http://localhost:3000')

class cbfs:
    def __init__(self):
        self.loaded_file = None
        self.qa = None
        self.chat_history = []
        self.answer = ""
        self.db_query = ""
        self.db_response = []

    def call_load_db(self, file):
        if not file:
            response = jsonify({"message": f"Loaded File: {self.loaded_file}"})
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Methods", "POST")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            return response
        
        file.save("temp.pdf")
        self.loaded_file = file.filename
        self.qa = load_db("temp.pdf", "stuff", 4)
        return jsonify({"message": f"Loaded File: {self.loaded_file}"})

    def convchain(self, query):
        if not query:
            return jsonify({"message": "Invalid query"}).headers.add("Access-Control-Allow-Origin", "http://localhost:3000")

        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer']
        return jsonify({
            "answer": self.answer,
            "chat_history": self.chat_history
        }).headers.add("Access-Control-Allow-Origin", "http://localhost:3000")

    def clr_history(self):
        self.chat_history = []
        return jsonify({"message": "Chat history cleared"}).headers.add("Access-Control-Allow-Origin", "http://localhost:3000")

cb = cbfs()

@app.route('/load_db', methods=['POST'])
def load_db_endpoint():
    if request.method == 'OPTIONS':
        return jsonify(), 200

    return cb.call_load_db(request.files.get('file')).headers.add("Access-Control-Allow-Origin", "http://localhost:3000")

@app.route('/conversation', methods=['POST'])
def conversation():
    if request.method == 'OPTIONS':
        return jsonify(), 200

    return cb.convchain(request.json.get('query')).headers.add("Access-Control-Allow-Origin", "http://localhost:3000")

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if request.method == 'OPTIONS':
        return jsonify(), 200

    return cb.clr_history().headers.add("Access-Control-Allow-Origin", "http://localhost:3000")

if __name__ == '__main__':
    app.run(debug=True)
