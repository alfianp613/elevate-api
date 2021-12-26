from re import I
from flask import Flask,request, jsonify, abort, send_file
from flask_cors import CORS
import json
from sentiment import *
from SVR import *

app = Flask(__name__)
CORS(app)

# datasentiment = [{'sentiment':['Positif','Negatif','Netral'],
#         'total':[100,70,30]}]

# forecast = [{'tanggal':['2021-12-21','2021-12-22','2021-12-23'],
#               'close':[46200,46150,46120]}]

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
            f = open(f'data sentiment/sentiment {coin}.json')
            sentimen = json.load(f)
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
            f = open(f'forecasting/forecasting {coin}.json')
            forecast = json.load(f)
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
        return send_file(f'wordcloud/wordcloud {koin}.png', mimetype=f'image/png')
        
if __name__ == '__main__':
    app.run(debug=True)