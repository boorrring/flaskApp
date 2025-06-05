from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load MongoDB URI from .env file

app = Flask(__name__, template_folder='../frontend/templates')

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["todo_database"]
collection = db["todo_items"]

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_id = request.form.get("itemId")
    item_name = request.form.get("itemName")
    item_desc = request.form.get("itemDescription")

    if not item_id or not item_name or not item_desc:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    collection.insert_one({
        "id": item_id,
        "name": item_name,
        "description": item_desc
    })

    return jsonify({"status": "success", "message": "Item saved successfully"}), 200

@app.route("/")
def home():
    return render_template('todo.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
