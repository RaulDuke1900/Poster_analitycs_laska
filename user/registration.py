import uuid

from flask import Flask, request, redirect
from user.user import User
import requests


TG_BOT_URL = 'https://t.me/Poster_analitycs_bot?start='  # link to my bot
APP_ID = '3310'  # from dev poster
APP_SECRET = '7a8e36e8e187d1afe477112c880902c4'  # from dev poster
REDIRECT_URL = 'http://gezha.space:5000/'  # from dev poster

app = Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def poster_oauth():
    secret_code = request.args['code']
    account = request.args['account']
    url = f'https://{account}.joinposter.com/api/v2/auth/access_token'  # poster instruction

    data = dict(application_id=(None, APP_ID),
                application_secret=(None, APP_SECRET),
                grant_type=(None, 'authorization_code'),
                redirect_uri=(None, REDIRECT_URL),
                code=(None, secret_code))
    response = requests.post(url=url, files=data)
    response.json()
    user_uuid: uuid.uuid4 = uuid.uuid4()
    User(token=response["access_token"], account_number=['account_number'])

    return redirect(f'{TG_BOT_URL}{user_uuid}')


if __name__ == '__main__':
    print(f'{TG_BOT_URL}{uuid.uuid4()}')
