import pandas as pd
from sqlalchemy import create_engine
import pymysql
import os
import sys

class MySQLConn():
    def __init__(self, app, db):
        self.app = app
        self.db = db
        db_connection_str = 'mysql+pymysql://root:{pwd}@mysql/{db}'.format(
            pwd=os.environ['MYSQL_ROOT_PASSWORD'],
            db=db,
        )
        self.conn = create_engine(db_connection_str)
    
    def debug(self, s):
        self.app.logger.debug(s)

    def query_data(self, query):
        '''Used when results returned'''
        return pd.read_sql(query, con=self.conn)
    
    def execute(self, query):
        '''Used when no results returned'''
        return self.conn.execute(query)

    def get_columns(self, table):
        query = 'DESCRIBE {db}.{table}'.format(db=self.db, table=table)
        return self.query_data(query).Field.tolist()

    def insert_into_table(self, table, data):
        columns = self.get_columns(table)
        insert_str = "INSERT INTO {db}.{table}".format(db=self.db, table=table)
        colnames, vals = '(', '('
        for col in columns:
            colnames += col + ','
            if col in data:
                vals += '"' + str(data[col]) + '",'
            else:
                vals += 'NULL,'

        query = insert_str+colnames[:-1]+') VALUES '+vals[:-1]+')'
        self.execute(query)
    
    def remove_from_table(self, table, condition):
        self.execute("DELETE FROM {db}.{table} WHERE ".format(
            db=self.db,
            table=table,
        ) + condition)


def add_strain():
    pass

def add_plasmid():
    pass

def add_gene():
    pass

def query_strain():
    pass

def query_plasmid():
    pass

def query_gene():
    pass

def connect_strain_plasmid():
    pass

def connect_plasmid_gene():
    pass