from flask import Blueprint, request, jsonify, g
from py_db import connection
import datetime
import re
import json
from app.models import Dsn
from app.models import TaskConfig
from app.main.utils import get_users, get_tables, get_comments
from collections import defaultdict
api = Blueprint('api', __name__, url_prefix='/api')
_match_table = re.compile("(\S+) ([t|T]\d+) ")

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

@api.route("/tasks/dsn", methods=["POST"])
def get_form():
    try:
        src = '-'.join([request.form['srcdsn'], request.form['srcuser'], request.form['srctable']])
        dst = '-'.join([request.form['dstdsn'], request.form['dstuser'], request.form['dsttable']])
        print(src, dst)
        outdate = datetime.datetime.today() + datetime.timedelta(days=1)
        resp = jsonify(result="success")
        resp.set_cookie('src', src, expires=outdate)
        resp.set_cookie('dst', dst, expires=outdate)
    except Exception as e:
        resp = jsonify(result="fail: %s" % e)
    return resp

@api.route("/mapping", methods=["GET"])
def get_mapping():
    dst_tab_name = g.__dst__[2]
    with connection(g.__dst__[0]) as db:
        db.dict_query("select * from %s where rownum <1" % dst_tab_name)
        columns = db.columns
    rs = {i.upper(): "" for i in columns}
    rs["tableName"] = "{} {} ".format(g.__src__[2], "t1")
    return jsonify(rs)

@api.route("/fields", methods=["GET"])
def get_fields():
    tmp = request.args.get("tableName")
    print(tmp)
    tab_name = tmp if tmp else "{} {}".format(g.__src__[2], "t1")
    with connection(g.__src__[0], debug=True) as db:
        sql = "select * from %s where rownum<1" % tab_name
        db.dict_query(sql)
        # columns = db.columns
        res = _match_table.findall(sql)
        tables = {j.lower(): i for i,j in res}
        user, name = g.__src__[1], g.__src__[2]
        comments = {}
        print(tables)
        for i in tables:
            name = tab_name = tables[i]
            db.dict_query(sql)
            print(user, name)
            com_tmp = {"{}.{}".format(i, k): v for k, v in get_comments(user, name, db).items()}
            comments.update(com_tmp)
    return jsonify(comments)

@api.route("/datas", methods=["GET"])
def get_datas():
    with connection(g.__src__[0]) as db:
        print(g.__src__[0])
        rs = db.dict_query("select * from %s where fssj is not null" % "{} {}".format(g.__src__[2], "t1"))
    dict_resp = defaultdict(list)
    for r in rs:
        for i in db.columns:
            dict_resp[i].append(r[i])
    return jsonify(dict_resp)

@api.route("/datas/<name>", methods=["GET"])
def get_a_data(name):
    with connection(g.__src__[0]) as db:
        print(g.__src__[0])
        rs = db.query("select %s from %s where fssj is not null and rownum<5" % (name, "{} {}".format(g.__src__[2], "t1")))
    list_resp = [i[0] for i in rs]
    return jsonify(list_resp)

@api.route("/tasks", methods=["POST"])
def create_task():
    # print(request.data)
    config = request.json
    name = config.pop('taskName')
    src_tab = config.pop('tableName')
    dst_tab = g.__dst__[2]
    if TaskConfig.query.filter_by(config=json.dumps(config)):
        return TaskConfig.query.filter_by(config='fail').first_or_404()
    else:
        task = TaskConfig(name=name, src=g.__src__[0], dst=g.__dst__[0], config=json.dumps(config), src_tab=src_tab, dst_tab=dst_tab)
        task.save()
    return 'ok'
