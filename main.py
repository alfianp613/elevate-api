from re import I
from flask import Flask,request, jsonify, abort, send_file
from flask_cors import CORS
import json
import pyrebase
from SVR import *
from sentiment import *

config = {'apiKey': "AIzaSyBF9zZqQBt2h0RJZN3Xubugse5Ba3qJLdw",
        'authDomain': "elevate-66775.firebaseapp.com",
        'projectId': "elevate-66775",
        'databaseURL': "https://elevate-66775-default-rtdb.asia-southeast1.firebasedatabase.app/",
        'storageBucket': "elevate-66775.appspot.com",
        'messagingSenderId': "1008765930388",
        'appId': "1:1008765930388:web:5ad1f3c8464d8f8d859d81",
        'measurementId': "G-0Q4Y5MFCVD"}
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
email = 'alfianp613@gmail.com'
password = 'DummyDummy631'
# Log the user in
user = auth.sign_in_with_email_and_password(email, password)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return '''<h1>Elevate API v1</h1>'''
	

@app.route('/api/datasentiment', methods=['POST'])
def req_data():
    if not request.json or not 'status' in request.json:
        abort(400)
    else:
        data = request.get_json()
        if data['status'] != 'minta datanya dong':
            abort(400)
        else:
            coin = data['koin']
            database = firebase.database()
            f = database.child("Sentiment").child(coin).get(user['idToken'])
            sentimen = dict(f.val())
            return jsonify(sentimen),201

@app.route('/api/forecast', methods=['POST'])
def req_forecast():
    if not request.json or not 'status' in request.json:
        abort(400)
    else:
        data = request.get_json()
        if data['status'] != 'minta datanya dong':
            abort(400)
        else:
            coin = data['koin']
            database = firebase.database()
            f = database.child("Forecast").child(coin).get(user['idToken'])
            forecast = dict(f.val())
            return jsonify(forecast),201

@app.route('/api/wordcloud', methods=['POST'])
def get_image():
    if not request.json or not 'status' in request.json:
        abort(400)
    data = request.get_json()
    if data['status'] != 'minta datanya dong':
            abort(400)
    else:
        koin = data['koin']
        storage = firebase.storage()
        storage.child(f'wordcloud/wordcloud {koin}.png').download(f"wordcloud/wordcloud {koin}.png")
        return send_file(f'wordcloud/wordcloud {koin}.png', mimetype=f'image/png')
@app.route('/api/update/forecast')
def update_forecast():
    koin = ['bitcoin','ethereum','binance coin','tether','solana',
        'cardano','xrp','usd coin','polkadot','dogecoin']
    for i in koin:
        forecast_SVR(i)
    return '''<h1>Data forecast berhasil di update</h1>'''

@app.route('/api/update/sentiment1')
def update_sentiment1():
    koin = ['bitcoin','ethereum','binance coin']
    for i in koin:
        sentimen(i)
    return '''<h1>Data sentiment1 berhasil di update</h1>'''
@app.route('/api/update/sentiment2')
def update_sentiment2():
    koin = ['tether','solana','cardano']
    for i in koin:
        sentimen(i)
    return '''<h1>Data sentiment2 berhasil di update</h1>'''
@app.route('/api/update/sentiment3')
def update_sentiment3():
    koin = ['xrp','usd coin','polkadot','dogecoin']
    for i in koin:
        sentimen(i)
    return '''<h1>Data sentiment3 berhasil di update</h1>'''
if __name__ == '__main__':
    app.run(debug=True)