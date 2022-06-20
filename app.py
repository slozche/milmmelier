from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://port99:H5WTfRwCkLeNBNbm@cluster0.5l5eay2.mongodb.net/?retryWrites=true&w=majority')
db = client.database;


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)