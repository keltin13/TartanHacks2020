from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

from app.database.scrape import *
from app.database.main import *

class User(UserMixin):
    # id = get_ids (all)
    #id = ['000001', '508234', '012345']
    # username = get_usernames (all)
    #username = ['keltin_7', 'RonSwanson', 'peepee']
    # password_hash = get_hashed_passwords
    #password_hash = ['kjnfd', '2436', '?']
    # bets = get_bet_table

    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return f'{self.username}, id: {self.id}'

    def set_password(self, password):
        self.check_password_hash = password#generate_password_hash(password)

    def check_password(self, password):
        return self.password_hash == password#check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @staticmethod
    def query_username(username):
        user = get_user_by_name(username,
                'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
        if user == None:
            return None
        return User(user['user_id'], user['username'], user['password_hash'])

    @staticmethod
    def query_user_id(id):
        user = get_user_by_id(id,
                'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
        if user == None:
            return None
        return User(id, user['username'], user['password_hash'])

    @staticmethod
    def query_user_bets(id):
        bets = get_user_bets(id,
                'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
        if bets == None:
            return []
        return bets

    @staticmethod
    def query_league_bets(league):
        live_bets = get_bets_by_league('NCAA',
                        'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
        return live_bets

@login.user_loader
def load_user(id):
    return User.query_user_id(id)
    #return User(id='012345',username='peepee',password_hash='?') #*******************
