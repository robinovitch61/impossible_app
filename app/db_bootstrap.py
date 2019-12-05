import mysql.connector
from mysql.connector import errorcode
import os

def bootstrap(db_name):
    cnx = mysql.connector.connect(
        user='root',
        password=os.environ['MYSQL_ROOT_PASSWORD'],
        host='mysql',
    )
    cursor = cnx.cursor()

    TABLES = {}
    TABLES['strain'] = (
        "CREATE TABLE `strain` ("
        "  `strain_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `created_by` varchar(100) DEFAULT NULL,"
        "  `creation_date` date NOT NULL,"
        "  `notes` text DEFAULT NULL,"
        "  PRIMARY KEY (`strain_id`)"
        ") ENGINE=InnoDB")

    TABLES['plasmid'] = (
        "CREATE TABLE `plasmid` ("
        "  `plasmid_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `insert` varchar(500) NULL,"
        "  `promoter` varchar(500) NULL,"
        "  `created_by` varchar(100) DEFAULT NULL,"
        "  `creation_date` date NOT NULL,"
        "  `notes` text DEFAULT NULL,"
        "  `files` text DEFAULT NULL,"
        "  PRIMARY KEY (`plasmid_id`)"
        ") ENGINE=InnoDB")

    TABLES['gene'] = (
        "CREATE TABLE `gene` ("
        "  `gene_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `description` text DEFAULT NULL,"
        "  `dna_seq` text DEFAULT NULL,"
        "  `created_by` varchar(100) DEFAULT NULL,"
        "  `creation_date` date NOT NULL,"
        "  `notes` text DEFAULT NULL,"
        "  `files` text DEFAULT NULL,"
        "  PRIMARY KEY (`gene_id`)"
        ") ENGINE=InnoDB")

    TABLES['strain_plasmid'] = (
        "CREATE TABLE `strain_plasmid` ("
        "  `strain_id` int(11) NOT NULL,"
        "  `plasmid_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`strain_id`)"
        ") ENGINE=InnoDB")

    TABLES['plasmid_gene'] = (
        "CREATE TABLE `plasmid_gene` ("
        "  `plasmid_id` int(11) NOT NULL,"
        "  `gene_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`plasmid_id`)"
        ") ENGINE=InnoDB")

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        except mysql.connector.Error as err:
            raise Exception("Failed creating database: {}".format(err))

    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            raise Exception(err)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()