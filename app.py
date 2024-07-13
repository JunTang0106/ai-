from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

APP_ID = '93570220'
API_KEY = '8n5C5w2abhQgiqlyrPOuV99V'
SECRET_KEY = '2BFgP0z7SXKrDDpDM1HInmiFO2Atf5aE'
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
SPEECH_API_URL = 'http://vop.baidu.com/server_api'
TRANSLATE_API_URL = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1'

def get_access_token():
    response = requests.post(TOKEN_URL, params={
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    })
    print('获取的access_token:', response.json())
    return response.json()['access_token']

@app.route('/recognize', methods=['POST'])
def recognize():
    audio_data = request.files['audio'].read()
    token = get_access_token()
    response = requests.post(SPEECH_API_URL, json={
        'format': 'pcm',
        'rate': 16000,
        'channel': 1,
        'cuid': APP_ID,
        'token': token,
        'len': len(audio_data),
        'speech': base64.b64encode(audio_data).decode('utf-8')
    })
    print('语音识别请求参数:', {
        'format': 'pcm',
        'rate': 16000,
        'channel': 1,
        'cuid': APP_ID,
        'token': token,
        'len': len(audio_data),
        'speech': base64.b64encode(audio_data).decode('utf-8')
    })
    print('语音识别响应:', response.json())
    return jsonify(response.json())

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json['text']
    token = get_access_token()
    response = requests.post(TRANSLATE_API_URL, json={
        'from': 'zh',
        'to': 'en',
        'q': text
    }, params={
        'access_token': token
    })
    print('翻译请求参数:', {
        'from': 'zh',
        'to': 'en',
        'q': text
    })
    print('翻译响应:', response.json())
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
