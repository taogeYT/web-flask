from flask import Blueprint, request, jsonify, render_template
from py_db import connection

page = Blueprint('page', __name__)
# db = connection('oracle://lyt:lyt@local:1521/xe')
# db2 = connection('oracle://jwdn:jwdn@local:1521/xe')

@page.route("/login", methods=["GET"])
def login():
    from app.model import db as init
    init.create_all()
    return render_template('login.html')

# @page.route('/', methods=['GET'])
# def index():
#     db.dict_query("select * from ssq_syc")
#     db2.dict_query("select * from ssq where rownum <1")
#     columns = db.columns
#     t1_columns = [(i,v) for i,v in enumerate(db2.columns)]
#     return render_template('index.html', columns=columns, t1_columns=t1_columns)

# @page.route("/sendjson", methods=["POST"])
# def get_data():
#     col_name = request.form['name']
#     datas = db2.query("select %s from ssq" % col_name)
#     return jsonify(name='id', value=datas[0][0])

@page.route("/test", methods=["GET"])
def test():
    return render_template('test.html')
