import mysql.connector
from mysql.connector import errorcode
import os
import random
import glob

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
        "  `strain_id` int(11) NOT NULL,"
        "  `description` text DEFAULT NULL,"
        "  `created_by` varchar(100) DEFAULT NULL,"
        "  `creation_date` date NOT NULL,"
        "  `notes` text DEFAULT NULL,"
        "  PRIMARY KEY (`strain_id`)"
        ") ENGINE=InnoDB")

    TABLES['plasmid'] = (
        "CREATE TABLE `plasmid` ("
        "  `plasmid_id` int(11) NOT NULL,"
        "  `_insert` varchar(500) NULL,"
        "  `promoter` varchar(500) NULL,"
        "  `created_by` varchar(100) DEFAULT NULL,"
        "  `creation_date` date NOT NULL,"
        "  `notes` text DEFAULT NULL,"
        # "  `files` text DEFAULT NULL,"
        "  PRIMARY KEY (`plasmid_id`)"
        ") ENGINE=InnoDB")

    TABLES['gene'] = (
        "CREATE TABLE `gene` ("
        "  `gene_id` int(11) NOT NULL,"
        "  `description` text DEFAULT NULL,"
        "  `dna_seq` text DEFAULT NULL,"
        "  `created_by` varchar(100) DEFAULT NULL,"
        "  `creation_date` date NOT NULL,"
        "  `notes` text DEFAULT NULL,"
        # "  `files` text DEFAULT NULL,"
        "  PRIMARY KEY (`gene_id`)"
        ") ENGINE=InnoDB")

    TABLES['strain_plasmid'] = (
        "CREATE TABLE `strain_plasmid` ("
        "  `strain_plasmid_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `strain_id` int(11) NOT NULL,"
        "  `plasmid_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`strain_plasmid_id`)"
        ") ENGINE=InnoDB")

    TABLES['plasmid_gene'] = (
        "CREATE TABLE `plasmid_gene` ("
        "  `plasmid_gene_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `plasmid_id` int(11) NOT NULL,"
        "  `gene_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`plasmid_gene_id`)"
        ") ENGINE=InnoDB")

    TABLES['files'] = (
        "CREATE TABLE `files` ("
        "  `file_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `file_name` text NOT NULL,"
        "  `path` text NOT NULL,"
        "  PRIMARY KEY (`file_id`)"
        ") ENGINE=InnoDB")

    TABLES['plasmid_files'] = (
        "CREATE TABLE `plasmid_files` ("
        "  `plasmid_files_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `plasmid_id` int(11) NOT NULL,"
        "  `file_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`plasmid_files_id`)"
        ") ENGINE=InnoDB")

    TABLES['gene_files'] = (
        "CREATE TABLE `gene_files` ("
        "  `gene_files_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `gene_id` int(11) NOT NULL,"
        "  `file_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`gene_files_id`)"
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

def populate(db):

    NUM_STRAINS = 4
    NUM_PLASMIDS = 6
    NUM_GENES = 10
    DEFAULT_FILENAMES = glob.glob(db.app.config['UPLOAD_FOLDER'] + "/*")
    NUM_DEF_FILES = len(DEFAULT_FILENAMES)
    # db.debug(repr(DEFAULT_FILENAMES))

    if not db.exists("strain"):
        strain_ids = list(range(NUM_STRAINS))
        strain_descriptions = ["strain_"+str(_id) for _id in strain_ids]
        strain_created_bys = ["Sample" for _ in range(len(strain_ids))]
        strain_creation_dates = ["2019-01-"+str(_id+10) for _id in strain_ids]
        strain_notes = ["notes_"+str(_id) for _id in strain_ids]

        for ii in range(len(strain_ids)):
            db.insert_into_table('strain', {
                'strain_id': strain_ids[ii],
                'description': strain_descriptions[ii],
                'created_by': strain_created_bys[ii],
                'creation_date': strain_creation_dates[ii],
                'notes': strain_notes[ii],
            })

    if not db.exists("plasmid"):
        plasmid_ids = list(range(NUM_PLASMIDS))
        plasmid_inserts = ["insert_"+str(_id) for _id in plasmid_ids]
        plasmid_promoter = ["promoter_"+str(_id) for _id in plasmid_ids]
        plasmid_created_bys = ["Sample" for _ in range(len(plasmid_ids))]
        plasmid_creation_dates = ["2019-01-"+str(_id+10) for _id in plasmid_ids]
        plasmid_notes = ["notes_"+str(_id) for _id in plasmid_ids]

        for ii in range(len(plasmid_ids)):
            db.insert_into_table('plasmid', {
                'plasmid_id': plasmid_ids[ii],
                '_insert': plasmid_inserts[ii],
                'promoter': plasmid_promoter[ii],
                'created_by': plasmid_created_bys[ii],
                'creation_date': plasmid_creation_dates[ii],
                'notes': plasmid_notes[ii],
            })

    if not db.exists("gene"):
        gene_ids = list(range(NUM_GENES))
        gene_descriptions = ["gene_"+str(_id) for _id in gene_ids]
        gene_dna_seqs = ["dna_seq_"+str(_id) for _id in gene_ids]
        gene_created_bys = ["Sample" for _ in range(len(gene_ids))]
        gene_creation_dates = ["2019-01-"+str(_id+10) for _id in gene_ids]
        gene_notes = ["notes_"+str(_id) for _id in gene_ids]

        for ii in range(len(gene_ids)):
            db.insert_into_table('gene', {
                'gene_id': gene_ids[ii],
                'description': gene_descriptions[ii],
                'dna_seq': gene_dna_seqs[ii],
                'created_by': gene_created_bys[ii],
                'creation_date': gene_creation_dates[ii],
                'notes': gene_notes[ii],
            })

    if not db.exists("strain_plasmid"):
        # randomly connect each strain with 2 to NUM_PLASMIDS plasmids
        for strain_id in range(NUM_STRAINS):
            plasmid_ids = []
            for _ in range(random.randint(2, NUM_PLASMIDS)):
                plasmid_id = random.randint(0, NUM_PLASMIDS)
                while plasmid_id in plasmid_ids:
                    plasmid_id = random.randint(0, NUM_PLASMIDS)
                plasmid_ids.append(plasmid_id)
                db.connect_strain_plasmid(strain_id, plasmid_id)

    if not db.exists("plasmid_gene"):
        # randomly connect each plasmid with 2 to NUM_GENES genes
        for plasmid_id in range(NUM_PLASMIDS):
            gene_ids = []
            for _ in range(random.randint(2, NUM_GENES)):
                gene_id = random.randint(0, NUM_GENES)
                while gene_id in gene_ids:
                    gene_id = random.randint(0, NUM_GENES)
                gene_ids.append(gene_id)
                db.connect_plasmid_gene(plasmid_id, gene_id)
    
    if not db.exists('files'):
        for path in DEFAULT_FILENAMES:
            file_name = path.split(os.path.sep)[-1]
            db.add_file(file_name, path)

    if not db.exists('plasmid_files'):
        # randomly associate between 1 and NUM_DEF_FILES files with each plasmid
        for plasmid_id in range(NUM_PLASMIDS):
            file_ids = []
            for _ in range(random.randint(1, NUM_DEF_FILES)):
                file_id = random.randint(0, NUM_DEF_FILES)
                while file_id in file_ids:
                    file_id = random.randint(0, NUM_DEF_FILES)
                file_ids.append(file_id)
                db.connect_plasmid_file(plasmid_id, file_id)

    if not db.exists('gene_files'):
        # randomly associate between 1 and NUM_DEF_FILES files with each gene
        for gene_id in range(NUM_GENES):
            file_ids = []
            for _ in range(random.randint(1, NUM_DEF_FILES)):
                file_id = random.randint(0, NUM_DEF_FILES)
                while file_id in file_ids:
                    file_id = random.randint(0, NUM_DEF_FILES)
                file_ids.append(file_id)
                db.connect_gene_file(gene_id, file_id)
    
    

