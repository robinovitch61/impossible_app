import mysql.connector
import os
from db_bootstrap import bootstrap

# Set up table schemas if they don't exist already
DB_NAME = 'microbes'
bootstrap(DB_NAME)

config = {
        'user': 'root',
        'password': os.environ['MYSQL_ROOT_PASSWORD'],
        'host': 'mysql',
        'port': os.environ['MYSQL_PORT'],
        'database': DB_NAME,
        'auth_plugin': 'mysql_native_password',
    }
connection = mysql.connector.connect(**config)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
