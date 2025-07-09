from flask import Flask, request, jsonify
from pymongo import MongoClient
import urllib.parse
import datetime

app = Flask(__name__)

# Safely encode username and password
username = urllib.parse.quote_plus("kandregulakalyani22")
password = urllib.parse.quote_plus("Kalyani@123")  # use your real password here

# Connection URI with correct cluster
uri = f"mongodb+srv://{username}:{password}@cluster0.gvla6bp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri)
db = client["github_events"]
collection = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    data['timestamp'] = datetime.datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    data['event'] = event_type
    collection.insert_one(data)
    return jsonify({"status": "success"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {'_id': 0}))
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000)
