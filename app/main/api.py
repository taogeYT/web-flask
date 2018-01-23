from flask import Blueprint, request, jsonify
from py_db import connection
import datetime
from app.models import Dsn
api = Blueprint('api', __name__, url_prefix='/api')

def get_tables(owner, db):
    sql = """
SELECT
    TABLE_NAME
FROM
    ALL_TABLES
WHERE
    OWNER = '%s'
""" % owner
    tables = db.query(sql)
    if tables:
        return [i[0] if i else None for i in tables]
    else:
        return None

def get_comments(owner, table, db):
    sql = """
SELECT
    COLUMN_NAME,
    COMMENTS
FROM
    all_col_comments
WHERE
    OWNER = '%s'
AND TABLE_NAME = '%s'
""" % (owner, table)
    return db.query(sql)

def get_users(db):
    sql = "select username from all_users"
    users = db.query(sql)
    if users:
        return [i[0] if i else None for i in users]
    else:
        return None

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
    list_dsn = []
    for dsn in Dsn.query.all():
        list_dsn.append(dsn.to_json())
    return jsonify(list_dsn)

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
        # print(request.form)
        # import pdb
        # pdb.set_trace()
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
