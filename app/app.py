import mysql.connector
import os
from db_bootstrap import bootstrap
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from db_helper import MySQLConn
import logging


# Set up table schemas if they don't exist already
# config = {
#         'user': 'root',
#         'password': os.environ['MYSQL_ROOT_PASSWORD'],
#         'host': 'mysql',
#         'port': os.environ['MYSQL_PORT'],
#         'database': DB_NAME,
#         'auth_plugin': 'mysql_native_password',
#     }
# connection = mysql.connector.connect(**config)
# cursor = connection.cursor()

from flask import Flask
app = Flask(__name__)

DB_NAME = 'microbes'
bootstrap(DB_NAME)
db = MySQLConn(app, DB_NAME)

@app.route('/')
def index():
    data = {
        'description': 'testing_desc',
        'dna_seq': 'asdfasfds',
        'created_by': 'leo',
        'creation_date': '2019-01-01',
        'notes': 'noestasfdasd',
        'files': 'asdfasf;adfasfasdf'
    }
    db.insert_into_table('gene', data)
    db.remove_from_table('gene', "gene_id > 10")
    app.logger.debug(db.query_data('SELECT * FROM microbes.gene'))
    return str(db.query_data('SELECT * FROM microbes.gene'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
