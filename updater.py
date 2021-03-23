from db import db_session
from db.shared import Shared
from config import *
import config


class Updater:

    def __init__(self):
        db_session.global_init(gdp('shared_data.db'))
        self.waiting = ''
        self.saved = ''

    def sign_in(self):
        if self.check_line_edits():
            return
        self.saved = config.WINDOW.get('ldtNickname').content.text
        self.send({
            'method': 'get',
            'add': '/' + config.WINDOW.get('ldtNickname').content.text,
            'password': config.WINDOW.get('ldtPassword').content.text,
        }, 'sign_in')

    def sign_up(self):
        if self.check_line_edits():
            return
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
        if config.NICKNAME:
            self.send({
                'method': 'put',
                'add': '/' + config.NICKNAME,
                'game_result': result,
            }, 'send_result')

    def send(self, data, wait):
        if self.waiting:
            return
        db_sess = db_session.create_session()
        request = db_sess.query(Shared).filter(Shared.id == 1).first()
        if request.data:
            return
        request.data = str(data)
        self.waiting = wait
        db_sess.merge(request)
        db_sess.commit()

    @staticmethod
    def recognize_response(response):
        errors = {
            'Empty request': 'server',
            'Bad request': 'server',
            'Nickname is already exists': 'exists_nickname',
            'OK': 'idle',
            'Incorrect password': 'incorrect_password',
            'Not found': 'unknown_nickname',
        }
        config.WINDOW.get('imgError').animation = errors.get(
            response['result'], 'unknown')

    @staticmethod
    def check_line_edits():
        if len(config.WINDOW.get('ldtNickname').content.text) < 4:
            config.WINDOW.get('imgError').animation = 'short_nickname'
            return True
        if len(config.WINDOW.get('ldtPassword').content.text) < 4:
            config.WINDOW.get('imgError').animation = 'short_password'
            return True

    def update(self):
        if not self.waiting:
            return
        db_sess = db_session.create_session()
        answer = db_sess.query(Shared).filter(Shared.id == 2).first()
        if not answer.data:
            return
        try:
            res = eval(answer.data)
            if self.waiting in ['sign_in', 'sign_up']:
                self.recognize_response(res)
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

            elif self.waiting == 'get_users':
                config.WINDOW.change_tab('rating')
                for i, user in enumerate(sorted(
                        res['users'], key=lambda x: x['rating'])[::-1][:10]):
                    user['number'] = i + 1
                    config.WINDOW.get('tarPlayer0' + str(i)).set_text(user)
        except Exception as e:
            print('ERROR', e)
            pass
        self.waiting = ''
        answer.data = ''
        db_sess.merge(answer)
        db_sess.commit()
