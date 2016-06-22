import pymysql
from pymysql.err import InternalError,ProgrammingError
class db(object):
    def __init__(self, db_name, host_name, user_name, passwd, db_type):
        self.db_name = db_name
        self.conn = pymysql.connect(host='192.168.1.191', user='ray1', passwd='abc19910601', db='mysql')
    def __enter__(self):
        self.cur = self.conn.cursor()
        return self
    def select_db(self):
        try:
            self.cur.execute('use '+self.db_name)
        except InternalError:
            #self.cur.execute('create table pages(id bigint,value bigint,primary key(id))')
            self.cur.execute('create database '+self.db_name)
            self.cur.execute('use '+self.db_name)
    def build_query(self, table, data):
        #status selector
        def isNumber(safe_check):
            numeric_type = set(['int', 'float', 'bigint', 'double'])
            if safe_check[1] in numeric_type and safe_check[0].lstrip('-').replace('.','',1).isdigit():
                return True
        col = ''
        value = ''
        for i in data:
            col += (i[0]+',')
            if isNumber(i[1:]):
                value += (i[1]+',')
            else:
                value += ('\"'+i[1]+'\",')
        return 'insert into '+table+' ('+col.rstrip(',')+') values ('+value.rstrip(',')+')'
    def build_table(self, table, value):
        '''
        Interactively construct a table
        '''
        pass
    def insert_db(self, table, data):
        self.select_db()
        query = self.build_query(table, data)
        self.cur.execute(query)
        self.cur.connection.commit()
    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()
