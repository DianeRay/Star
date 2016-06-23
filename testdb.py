from db import db
with db('test_db', '192.168.1.191', 'ray1', 'abc19910601') as mysql_db:
    # values: ((columns, value, type),...)
    values = (('id','2','int'),('value','2','int'))
    mysql_db.insert_db('test_table', values)
