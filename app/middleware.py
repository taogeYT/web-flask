from flask import request, current_app, g
from app.models import Dsn


def logined_user():
    src_cookie = request.cookies.get('src')
    dst_cookie = request.cookies.get('dst')
    g.__src__ = Dsn.find_by_cookie(src_cookie)
    g.__dst__ = Dsn.find_by_cookie(dst_cookie)
