from flask import Blueprint, request, jsonify, g
from py_db import connection
import datetime
from app.models import Dsn
from app.main.utils import get_users, get_tables
from collections import defaultdict
api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/connections", methods=["POST"])
def db_connect_test():
    try:
        name = request.form['name'].strip()
        if not name:
            raise Exception("输入正确的数据库名称")
        driver = request.form['driver'].strip()
        dsn = request.form['dsn'].strip()
        if not dsn:
            dsn = Dsn.query.filter_by(name=name).first()
            if not dsn:
                raise Exception("无效的数据库连接")
            else:
                dsn = dsn.dsn
        print(dsn)
        with connection(dsn) as db:
            db.connect.connect()
            users = get_users(db)
    except Exception as reason:
        return jsonify(result="fail: %s" % reason)
    if not Dsn.query.filter_by(name=name).first():
        Dsn(name=name, driver=driver, dsn=dsn)
    return jsonify(result="success", users=users)

@api.route("/connections", methods=["GET"])
def get_connection_name():
    dict_dsn = {}
    for dsn in Dsn.query.all():
        dict_dsn[dsn.name] = dsn.to_json()
    return jsonify(dict_dsn)

@api.route("/connections/<name>", methods=["GET"])
def get_connection_config(name):
    dsn = Dsn.query.filter_by(name=name).first()
    if not dsn:
        return jsonify(driver=None, dsn=dsn)
    return jsonify(dsn.to_json())

@api.route("/connections/<name>/<user>", methods=["GET"])
def get_connection_tables(name, user):
    dsn = Dsn.query.filter_by(name=name).first()
    if not dsn:
        return jsonify(driver=None, dsn=dsn)
    with connection(dsn.dsn) as db:
        tables = get_tables(user, db)
    return jsonify(tables=tables)

@api.route("/tasks", methods=["POST"])
def get_form():
    try:
        src = '-'.join([request.form['srcdsn'], request.form['srctable']])
        dst = '-'.join([request.form['dstdsn'], request.form['dsttable']])
        print(src, dst)
        outdate = datetime.datetime.today() + datetime.timedelta(days=1)
        resp = jsonify(result="success")
        resp.set_cookie('src', src, expires=outdate)
        resp.set_cookie('dst', dst, expires=outdate)
    except Exception as e:
        resp = jsonify(result="fail: %s" % e)
    return resp

@api.route("/fields", methods=["GET"])
def get_fields():
    with connection(g.__dst__[0]) as db:
        print(g.__dst__[0])
        db.dict_query("select * from %s where rownum <1" % g.__dst__[1])
        columns = db.columns
    return jsonify({i: "" for i in columns})

@api.route("/datas", methods=["GET"])
def get_datas():
    with connection(g.__src__[0]) as db:
        print(g.__src__[0])
        rs = db.dict_query("select * from %s where fssj is not null" % g.__src__[1])
    dict_resp = defaultdict(list)
    for r in rs:
        for i in db.columns:
            dict_resp[i].append(r[i])
    return jsonify(dict_resp)

@api.route("/datas/<name>", methods=["GET"])
def get_a_data(name):
    with connection(g.__src__[0]) as db:
        print(g.__src__[0])
        rs = db.query("select %s from %s where fssj is not null and rownum<5" % (name, g.__src__[1]))
    list_resp = [i[0] for i in rs]
    return jsonify(list_resp)
