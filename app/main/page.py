from flask import Blueprint, request, jsonify, render_template, g, url_for, redirect
from py_db import connection

page = Blueprint('page', __name__)
# db = connection('oracle://lyt:lyt@local:1521/xe')
# db2 = connection('oracle://jwdn:jwdn@local:1521/xe')

@page.route("/login", methods=["GET"])
def login():
    # from app.models import db as init
    # init.create_all()
    return render_template('login.html')

@page.route('/task/config', methods=['GET'])
def index():
    if g.__src__ is None or g.__dst__ is None:
        return redirect(url_for('page.login'))
    with connection(g.__src__[0]) as db:
        print(g.__src__[0])
        db.dict_query("select * from %s" % g.__src__[1])
        t1_columns = [(i,v) for i,v in enumerate(db.columns)]
    with connection(g.__dst__[0]) as db:
        print(g.__dst__[0])
        db.dict_query("select * from %s where rownum <1" % g.__dst__[1])
        columns = db.columns
    return render_template('index.html', columns=columns, t1_columns=t1_columns)

@page.route("/sendjson", methods=["POST"])
def get_data():
    col_name = request.form['name']
    with connection(g.__src__[0]) as db:
        datas = db.query("select %s from %s" % (col_name, g.__src__[1]))
    return jsonify(name='id', value=datas[0][0])

@page.route("/test", methods=["GET"])
def test():
    return render_template('test.html')
