"""
数据库资源查询
"""


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
