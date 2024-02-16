from user.user import User
from datetime import datetime


if __name__ == '__main__':
    laska: User = User.load_from_file('laska.pkl')
    params = {'token': '063653:5909958edcfe4585f2d20e76893b5b56'}
    info = laska.get_application_info(params)

    print(info)
