from db import db_session
from db.shared import Shared
from config import *
import config


class Updater:

    def __init__(self):
        db_session.global_init(gdp('shared_data.db'))
        self.db_sess = db_session.create_session()
        self.waiting = ''
        self.saved = ''

    def sign_in(self):
        self.saved = config.WINDOW.get('ldtNickname').content.text
        self.send({
            'method': 'get',
            'add': '/' + config.WINDOW.get('ldtNickname').content.text,
            'nickname': config.WINDOW.get('ldtNickname').content.text,
            'password': config.WINDOW.get('ldtPassword').content.text,
        }, 'sign_in')

    def sign_up(self):
        self.saved = config.WINDOW.get('ldtNickname').content.text
        self.send({
            'method': 'post',
            'add': '',
            'nickname': config.WINDOW.get('ldtNickname').content.text,
            'password': config.WINDOW.get('ldtPassword').content.text,
        }, 'sign_up')

    def get_users(self):
        self.send({
            'method': 'get',
            'add': '',
        }, 'get_users')

    def send_result(self, result):
        self.send({
            'method': 'update',
            'add': '/' + config.NICKNAME,
            'game_result': result,
        }, 'send_result')

    def send(self, data, wait):
        if self.waiting:
            return
        request = self.db_sess.query(Shared).filter(Shared.id == 1).first()
        if request.data:
            return
        request.data = str(data)
        self.waiting = wait
        self.db_sess.merge(request)
        self.db_sess.commit()

    @staticmethod
    def prepare_rating(number, user):
        number = ('0' + str(number + 1)).ljust(3, ' ')
        nickname = str(user['nickname']).ljust(15, ' ')
        rating = str(user['rating']).ljust(12, ' ')
        best = str(user['best']).ljust(8, ' ')
        created = str(user['created'])
        return number + nickname + rating + best + created

    def update(self):
        if not self.waiting:
            return
        answer = self.db_sess.query(Shared).filter(Shared.id == 2).first()
        if not answer.data:
            return
        res = eval(answer.data)
        if self.waiting in ['sign_in', 'sign_up']:
            if res['result'] == 'OK':
                config.NICKNAME = self.saved
                del self.saved
                config.WINDOW.tabs['login'] = config.WINDOW.tabs['profile']
                config.WINDOW.change_tab('profile')
                user = res['user']
                config.WINDOW.get('txtNickname').set_text(user['nickname'])
                config.WINDOW.get('txtRating').set_text(user['rating'])
                config.WINDOW.get('txtBest').set_text(user['best'])
                config.WINDOW.get('txtCreated').set_text(user['created'])
            else:
                print(res)
        elif self.waiting == 'get_users':
            config.WINDOW.change_tab('rating')
            for i, user in enumerate(sorted(res['users'], reverse=True,
                                            key=lambda x: x['rating'])[:10]):
                config.WINDOW.get('txtPlayer_0' + str(i)).set_text(
                    self.prepare_rating(i, user))

        self.waiting = ''
        answer.data = ''
        self.db_sess.merge(answer)
        self.db_sess.commit()
