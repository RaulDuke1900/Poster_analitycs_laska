import os
import requests
import uuid

from flask import Flask, request, redirect

from constants import URL_FOR_OAUTH, POSTER_ANALITYCS_APP_ID, POSTER_ANALITYCS_APP_TOKEN

app = Flask(__name__)
project_root = os.path.dirname(os.path.abspath(__file__))

@app.route('/poster_reg/', methods=['GET', 'HEAD'])
def registration():
    secret_code = request.args['code']
    account = request.args['account']
    deep_link = uuid.uuid4()
    url = f'https://{account}.joinposter.com/api/v2/auth/access_token'
    data = dict(application_id=(None, POSTER_ANALITYCS_APP_ID), application_secret=(None, POSTER_ANALITYCS_APP_TOKEN),
                grant_type=(None, 'authorization_code'), redirect_uri=(None, URL_FOR_OAUTH), code=(None, secret_code))
    response = requests.post(url=url, files=data)
    with open(f'{project_root}/test_reg.json', 'a') as file:
        file.write(response.text)
        file.write('\n')
    return redirect(f'https://t.me/Poster_analitycs_bot?start={deep_link}')


@app.route('/',methods=['GET'])
def hello():
    return 'This is landing page Poster_analitycs_bot!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
