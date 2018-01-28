from flask import Blueprint, request, jsonify, render_template, g, url_for, redirect
from py_db import connection
from app.main.utils import get_comments

page = Blueprint('page', __name__)
# db = connection('oracle://lyt:lyt@local:1521/xe')
# db2 = connection('oracle://jwdn:jwdn@local:1521/xe')

@page.route("/init", methods=["GET"])
def init_db():
    from app.models import db as init
    init.create_all()
    return 'ok'

@page.route("/login", methods=["GET"])
def login():
    # from app.models import db as init
    # init.create_all()
    return render_template('login.html')

@page.route('/task/config', methods=['GET'])
def index():
    if g.__src__ is None or g.__dst__ is None:
        return redirect(url_for('page.login'))
    print("connecting...  ", g.__src__[0])
    with connection(g.__src__[0]) as db:
        tab_name = g.__src__[2]
        user, name = g.__src__[1], g.__src__[2]
        db.dict_query("select * from %s where rownum<1" % tab_name)
        comments = get_comments(user, name, db)
        print(comments)
        # src_columns = [(i,v) for i,v in enumerate(db.columns)]
    print("connecting...  ", g.__dst__[0])
    with connection(g.__dst__[0]) as db:
        tab_name = g.__dst__[2]
        user, name = g.__dst__[1], g.__dst__[2]
        db.dict_query("select * from %s where rownum <1" % tab_name)
        # columns = db.columns
        columns = get_comments(user, name, db)
    return render_template('index.html', columns=columns, src_columns=comments)

@page.route("/sendjson", methods=["POST"])
def get_data():
    col_name = request.form['name']
    with connection(g.__src__[0]) as db:
        datas = db.query("select %s from %s" % (col_name, g.__src__[2]))
    return jsonify(name='id', value=datas[0][0])

@page.route("/task/home", methods=["GET"])
def task_home():
    return render_template('home.html')

@page.route("/test", methods=["GET"])
def test():
    return render_template('test.html')
