from user.user import User
from datetime import datetime
from config.config import load_config


if __name__ == '__main__':
    cfg = load_config()
    user = User(token=cfg.poster_token, account_number=cfg.poster_account)
