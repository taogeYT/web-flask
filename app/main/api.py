from flask import Blueprint, request, jsonify
from py_db import connection
from app.model import Dsn
api = Blueprint('api', __name__, url_prefix='/api')


@api.route("/test", methods=["POST"])
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
    except Exception as reason:
        return jsonify(result="fail: %s" % reason)
    if not Dsn.query.filter_by(name=name).first():
        Dsn(name=name, driver=driver, dsn=dsn)
    return jsonify(result="success")

@api.route("/db_history", methods=["GET"])
def get_connection_name():
    list_dsn = []
    for dsn in Dsn.query.all():
        list_dsn.append(dsn.to_json())
    return jsonify(list_dsn)

@api.route("/db_history", methods=["POST"])
def get_connection_config():
    name = request.form["name"].strip()
    dsn = Dsn.query.filter_by(name=name).first()
    if not dsn:
        return jsonify(driver=None, dsn=dsn)
    return jsonify(dsn.to_json())

@api.route("/form", methods=["POST"])
def get_form():
    print(request.form)
    return jsonify(request.form)
