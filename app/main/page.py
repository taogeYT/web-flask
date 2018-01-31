from flask import Blueprint, render_template, g, url_for, redirect
from py_db import connection
from app.main.utils import get_comments
from flask import current_app
page = Blueprint('page', __name__)


@page.route("/init", methods=["GET"])
def init_db():
    from app.models import db as init
    init.create_all()
    return 'db init ok'

@page.route("/login", methods=["GET"])
def login():
    return render_template('login.html')

@page.route('/task/config', methods=['GET'])
def index():
    if g.__src__ is None or g.__dst__ is None:
        return redirect(url_for('page.login'))
    current_app.logger.warn("connecting...  %s" % g.__src__[0])
    with connection(g.__src__[0]) as db:
        tab_name = g.__src__[2]
        user, name = g.__src__[1], g.__src__[2]
        db.dict_query("select * from %s where rownum<1" % tab_name)
        comments = get_comments(user, name, db)
    with connection(g.__dst__[0]) as db:
        tab_name = g.__dst__[2]
        user, name = g.__dst__[1], g.__dst__[2]
        db.dict_query("select * from %s where rownum <1" % tab_name)
        columns = get_comments(user, name, db)
    return render_template('index.html', columns=columns, src_columns=comments)

@page.route("/task/home", methods=["GET"])
def task_home():
    return render_template('home.html')

@page.route("/test", methods=["GET"])
def test():
    return render_template('test.html')

@page.route("/db", methods=["GET"])
def db_test():
    from app import db
    db2 = connection(db)
    db2.insert("insert into user values(1,'ok')")
    return 'ok'
