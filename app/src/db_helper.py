import pandas as pd
from sqlalchemy import create_engine
import pymysql
import os
import sys

BASE_QUERY_STRING = """
SELECT * FROM {db}.{table}
WHERE 1=1"""

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
        if "{db}" in query:
            query = query.format(db=self.db)
        return pd.read_sql(query, con=self.conn)
    
    def get_unique_ids(self, table):
        id_col = "{table}_id".format(table=table)
        query = "SELECT DISTINCT {id_col} FROM {db}.{table}".format(
            id_col=id_col,
            table=table,
            db=self.db
        )
        return self.query_data(query)[id_col].tolist()
        
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
        self.debug("\n" + query + "\n")
        self.execute(query)
    
    def remove_from_table(self, table, condition):
        self.execute("DELETE FROM {db}.{table} WHERE ".format(
            db=self.db,
            table=table,
        ) + condition)

    def exists(self, table, conditions=[]):
        query = BASE_QUERY_STRING.format(db=self.db, table=table)
        for cond in conditions:
            query += '\nAND {cond}'.format(cond=cond)
        return len(self.query_data(query)) > 0

    def connect_strain_plasmid(self, strain_id, plasmid_id):
        # if not already connected and plasmid exists, connect
        already_conn = self.exists("strain_plasmid", [
                f"strain_id={strain_id}",
                f"plasmid_id={plasmid_id}",
            ])

        plasmid_exists = self.exists("plasmid", [
                f"plasmid_id={plasmid_id}",
            ])

        if not already_conn and plasmid_exists:
            self.insert_into_table("strain_plasmid", {
                "strain_id": strain_id,
                "plasmid_id": plasmid_id,
            })

    def connect_plasmid_gene(self, plasmid_id, gene_id):
        # if not already connected and gene exists, connect
        already_conn = self.exists("plasmid_gene", [
                f"plasmid_id={plasmid_id}",
                f"gene_id={gene_id}",
            ])

        gene_exists = self.exists("gene", [
                f"gene_id={gene_id}",
            ])

        if not already_conn and gene_exists:
            self.insert_into_table("plasmid_gene", {
                "plasmid_id": plasmid_id,
                "gene_id": gene_id,
            })
    
    def add_file(self, file_name, path):
        already_exists = self.exists("files", [
                f"file_name='{file_name}'",
                f"path='{path}'",
            ])

        if not already_exists:
            self.insert_into_table("files", {
                "file_name": file_name,
                "path": path,
            })

    def connect_plasmid_file(self, plasmid_id, file_id):
        # if not already connected and file exists, connect
        already_conn = self.exists("plasmid_files", [
                f"plasmid_id={plasmid_id}",
                f"file_id={file_id}",
            ])

        file_exists = self.exists("files", [
                f"file_id={file_id}",
            ])

        if not already_conn and file_exists:
            self.insert_into_table("plasmid_files", {
                "plasmid_id": plasmid_id,
                "file_id": file_id,
            })

    def connect_gene_file(self, gene_id, file_id):
        # if not already connected and file exists, connect
        already_conn = self.exists("gene_files", [
                f"gene_id={gene_id}",
                f"file_id={file_id}",
            ])

        file_exists = self.exists("files", [
                f"file_id={file_id}",
            ])

        if not already_conn and file_exists:
            self.insert_into_table("gene_files", {
                "gene_id": gene_id,
                "file_id": file_id,
            })
