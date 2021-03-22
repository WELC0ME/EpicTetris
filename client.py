import time
import requests
from db import db_session
from db.shared import Shared
from config import *

db_session.global_init(gdp('shared_data.db'))
db_sess = db_session.create_session()
for shared in db_sess.query(Shared).all():
    db_sess.delete(shared)
    db_sess.commit()
db_sess.add(Shared(data=''))
db_sess.commit()
db_sess.add(Shared(data=''))
db_sess.commit()
while True:
    db_sess = db_session.create_session()
    request = db_sess.query(Shared).filter(Shared.id == 1).first()
    answer = db_sess.query(Shared).filter(Shared.id == 2).first()
    if request.data and not answer.data:
        send = eval(request.data)
        try:
            res = str(getattr(requests, send['method'])(
                SERVER + send['add'], json=send).json())
        except Exception:
            res = str({
                'result': 'unknown error'
            })
        answer.data = res
        db_sess.merge(answer)
        db_sess.commit()
        request.data = ''
        db_sess.merge(request)
        db_sess.commit()
    time.sleep(0.1)
