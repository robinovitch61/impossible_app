import mysql.connector
import os
from src.db_bootstrap import bootstrap, populate
from src.db_helper import MySQLConn
from src.forms import StrainAddForm, StrainDeleteForm, PlasmidAddForm, PlasmidDeleteForm, GeneAddForm, GeneDeleteForm, UploadForm
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import logging
from werkzeug.utils import secure_filename

from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

# upload folder
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']

# secret key for CSRF
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# on app startup
DB_NAME = 'microbes'
bootstrap(DB_NAME)
db = MySQLConn(app, DB_NAME)
populate(db)

@app.route('/')
def index():
    return redirect("/strain")

@app.route('/strain', methods=("GET", "POST"))
def strain():

    app.logger.debug(db.query_data("SELECT * FROM {db}.strain_plasmid"))

    # add strain
    strain_form = StrainAddForm(request.form)
    if strain_form.validate_on_submit():
        # overwrite row if exists, if not present assign new id
        all_ids = db.get_unique_ids("strain")

        strain_id = strain_form.strain_id.data.strip()
        valid_id = (strain_id != ""
            and strain_id.isnumeric()
            and int(strain_id) >= 0)
        if not valid_id:
            if len(all_ids):
                strain_id = max(all_ids)+1
            else:
                strain_id = 0
        elif int(strain_id) in all_ids:
            for table in ("strain", "strain_plasmid"):
                db.remove_from_table(table, 'strain_id = {}'.format(strain_del_id))
            strain_id = int(strain_id)
        else:
            strain_id = int(strain_id)

        # add data
        data = {
            'strain_id': strain_id,
            'description': strain_form.description.data,
            'created_by': strain_form.created_by.data,
            'creation_date': strain_form.creation_date.data,
            'notes': strain_form.notes.data,
        }
        db.insert_into_table('strain', data)

        # associate plasmid(s) with strain
        plasmid_ids = strain_form.plasmid_ids.data\
            .strip()\
            .replace(' ', '')\
            .replace('"', '')\
            .replace("'", "")\
            .split(",")
        if len(plasmid_ids):
            for plasmid_id in plasmid_ids:
                if plasmid_id.isnumeric():
                    app.logger.debug(plasmid_id)
                    db.connect_strain_plasmid(strain_id, plasmid_id)

        return redirect('/strain')

    # delete strain
    strain_del_form = StrainDeleteForm(request.form)
    if strain_del_form.validate_on_submit():
        strain_del_id = strain_del_form.strain_del_id.data
        # remove both strain info and strain -> plasmid info
        for table in ("strain", "strain_plasmid"):
            db.remove_from_table(table, 'strain_id = {}'.format(strain_del_id))
        return redirect('/strain')

    df_strain = db.query_data("SELECT * FROM {db}.strain")

    return render_template(
        'strain.html',
        strain=df_strain.to_html(header="true", index=False, table_id="strain_table"),
        strain_form=strain_form,
        strain_del_form=strain_del_form,
    )

@app.route('/plasmid', methods=("GET", "POST"))
def plasmid():

    # add plasmid
    plasmid_form = PlasmidAddForm(request.form)    
    if plasmid_form.validate_on_submit():
        # overwrite row if exists, if not present assign new id
        all_ids = db.get_unique_ids("plasmid")

        plasmid_id = plasmid_form.plasmid_id.data.strip()
        # if invalid input, assign new id
        valid_id = (plasmid_id != ""
            and plasmid_id.isnumeric()
            and int(plasmid_id) >= 0)
        if not valid_id:
            if len(all_ids):
                plasmid_id = max(all_ids)+1
            else:
                plasmid_id = 0
        elif int(plasmid_id) in all_ids:
            for table in ("plasmid", "strain_plasmid", "plasmid_gene"):
                db.remove_from_table(table, 'plasmid_id = {}'.format(plasmid_del_id))
            plasmid_id = int(plasmid_id)
        else:
            plasmid_id = int(plasmid_id)

        # add data
        data = {
            'plasmid_id': plasmid_id,
            '_insert': plasmid_form.insert.data,
            'promoter': plasmid_form.promoter.data,
            'created_by': plasmid_form.created_by.data,
            'creation_date': plasmid_form.creation_date.data,
            'notes': plasmid_form.notes.data,
        }
        db.insert_into_table('plasmid', data)

        # associate gene(s) with plasmid
        gene_ids = plasmid_form.gene_ids.data\
            .strip()\
            .replace(' ', '')\
            .replace('"', '')\
            .replace("'", "")\
            .split(",")
        if len(gene_ids):
            for gene_id in gene_ids:
                if gene_id.isnumeric():
                    db.connect_plasmid_gene(plasmid_id, gene_id)

        return redirect('/plasmid')

    # delete plasmid
    plasmid_del_form = PlasmidDeleteForm(request.form)
    if plasmid_del_form.validate_on_submit():
        plasmid_del_id = plasmid_del_form.plasmid_del_id.data
        # remove both plasmid info and plasmid -> plasmid info
        for table in ("plasmid", "strain_plasmid", "plasmid_gene"):
            db.remove_from_table(table, 'plasmid_id = {}'.format(plasmid_del_id))
        return redirect('/plasmid')
    
    df_plasmid = db.query_data("SELECT * FROM {db}.plasmid")

    return render_template(
        'plasmid.html',
        plasmid=df_plasmid.to_html(header="true", index=False, table_id="plasmid_table"),
        plasmid_form=plasmid_form,
        plasmid_del_form=plasmid_del_form,
    )

@app.route('/gene', methods=("GET", "POST"))
def gene():

    # add gene
    gene_form = GeneAddForm(request.form)
    if gene_form.validate_on_submit():
        # overwrite row if exists, if not present assign new id
        all_ids = db.get_unique_ids("gene")

        gene_id = gene_form.gene_id.data.strip()
        # if invalid input, assign new id
        valid_id = (gene_id != ""
            and gene_id.isnumeric()
            and int(gene_id) >= 0)
        if not valid_id:
            if len(all_ids):
                gene_id = max(all_ids)+1
            else:
                gene_id = 0
        elif int(gene_id) in all_ids:
            for table in ("gene", "plasmid_gene"):
                db.remove_from_table('gene', 'gene_id = {}'.format(gene_id))
            gene_id = int(gene_id)
        else:
            gene_id = int(gene_id)

        # add data
        data = {
            'gene_id': gene_id,
            'description': gene_form.description.data,
            'dna_seq': gene_form.dna_seq.data,
            'created_by': gene_form.created_by.data,
            'creation_date': gene_form.creation_date.data,
            'notes': gene_form.notes.data,
        }
        db.insert_into_table('gene', data)

        return redirect('/gene')

    # delete gene
    gene_del_form = GeneDeleteForm(request.form)
    if gene_del_form.validate_on_submit():
        gene_id = gene_del_form.gene_id.data
        for table in ("gene", "plasmid_gene"):
            db.remove_from_table('gene', 'gene_id = {}'.format(gene_id))
        return redirect('/gene')

    # upload files for gene
    gene_file_form = UploadForm(request.form)
    if gene_file_form.validate_on_submit():
        file_names = request.files.getlist(gene_file_form.files.name)
        all_files = []
        app.logger.debug(file_names)
        for _file in file_names:
            file_name = secure_filename(_file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            all_files.append(full_path)
            _file.save(full_path)
        app.logger.debug(all_files)
        return redirect('/gene')

    df_gene = db.query_data("SELECT * FROM {db}.gene")

    return render_template(
        'gene.html',
        gene=df_gene.to_html(header="true", index=False, table_id="gene_table"),
        gene_form=gene_form,
        gene_del_form=gene_del_form,
    )

@app.route('/strain/<strain_id>', methods=("GET", "POST"))
def strain_view(strain_id):
    # deliver:
    # - id and subtitle (description)
    # - table of associated children (plasmids)
    # - table of associated parents (N/A)
    # - list of associated file names and paths (N/A)
    # - upload form (N/A)

    app.logger.debug(db.query_data("SELECT * FROM {db}.strain_plasmid"))

    valid_ids = db.get_unique_ids("strain")
    if not strain_id.isnumeric() or int(strain_id) not in valid_ids:
        return redirect('/strain')

    description = db.query_data(
        "SELECT description FROM {db}.strain WHERE strain_id = {id}".format(
            db=db.db,
            id=strain_id,
        )).description.values[0]
    
    df_plasmids = db.query_data("""
        SELECT * FROM {db}.plasmid
        WHERE plasmid_id IN (
            SELECT plasmid_id FROM {db}.strain_plasmid
            WHERE strain_id = {id}
        )
    """.format(db=db.db, id=strain_id))

    return render_template(
        "zoom_view.html",
        title="Strain " + str(strain_id),
        zoom_id=strain_id,
        subtitle=description,
        df_children=df_plasmids.to_html(header="true", index=False, table_id="plasmid_table"),
        df_parents=None,
        file_path_pairs=None,
        upload_form=None,
    )

@app.route('/plasmid/<plasmid_id>', methods=("GET", "POST"))
def plasmid_view(plasmid_id):
    # deliver:
    # - id and subtitle (insert, promoter)
    # - table of associated children (genes)
    # - table of associated parents (strains)
    # - list of associated file names and paths
    # - upload form

    valid_ids = db.get_unique_ids("plasmid")
    if not plasmid_id.isnumeric() or int(plasmid_id) not in valid_ids:
        return redirect('/plasmid')

    # upload files for plasmid
    plasmid_file_form = UploadForm(request.form)
    if plasmid_file_form.validate_on_submit():
        file_names = request.files.getlist(plasmid_file_form.files.name)
        for _file in file_names:
            file_name = secure_filename(_file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            _file.save(full_path)
            db.add_file(file_name, full_path)
            file_id = db.get_file_id(full_path)
            db.connect_plasmid_file(plasmid_id, file_id)
        return redirect('/plasmid/{id}'.format(id=plasmid_id))

    df_res = db.query_data(
        "SELECT _insert, promoter FROM {db}.plasmid WHERE plasmid_id = {id}".format(
            db=db.db,
            id=plasmid_id,
        ))
    insert = df_res._insert.values[0]
    promoter = df_res.promoter.values[0]
    
    df_strains = db.query_data("""
        SELECT * FROM {db}.strain
        WHERE strain_id IN (
            SELECT strain_id FROM {db}.strain_plasmid
            WHERE plasmid_id = {id}
        )
    """.format(db=db.db, id=plasmid_id))

    df_genes = db.query_data("""
        SELECT * FROM {db}.gene
        WHERE gene_id IN (
            SELECT gene_id FROM {db}.plasmid_gene
            WHERE plasmid_id = {id}
        )
    """.format(db=db.db, id=plasmid_id))

    df_files = db.query_data("""
        SELECT * FROM {db}.files
        WHERE file_id IN (
            SELECT file_id FROM {db}.plasmid_files
            WHERE plasmid_id = {id}
        )
    """.format(db=db.db, id=plasmid_id))
    files = df_files.file_name.tolist()
    paths = df_files.path.tolist()
    file_path_pairs = [(f, p) for f, p in zip(files, paths)]

    return render_template(
        "zoom_view.html",
        title="Plasmid " + str(plasmid_id),
        zoom_id=plasmid_id,
        subtitle=insert + '; ' + promoter,
        df_children=df_genes.to_html(header="true", index=False, table_id="gene_table"),
        df_parents=df_strains.to_html(header="true", index=False, table_id="strain_table"),
        file_path_pairs=file_path_pairs,
        upload_form=plasmid_file_form,
    )

@app.route('/gene/<gene_id>', methods=("GET", "POST"))
def gene_view(gene_id):
    # deliver:
    # - id and subtitle (description)
    # - table of associated children (N/A)
    # - table of associated parents (plasmids)
    # - list of associated file names and paths
    # - upload form

    valid_ids = db.get_unique_ids("gene")
    if not gene_id.isnumeric() or int(gene_id) not in valid_ids:
        return redirect('/gene')

    # upload files for gene
    gene_file_form = UploadForm(request.form)
    if gene_file_form.validate_on_submit():
        file_names = request.files.getlist(gene_file_form.files.name)
        for _file in file_names:
            file_name = secure_filename(_file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            _file.save(full_path)
            db.add_file(file_name, full_path)
            file_id = db.get_file_id(full_path)
            db.connect_gene_file(gene_id, file_id)
        return redirect('/gene/{id}'.format(id=gene_id))

    description = db.query_data(
        "SELECT description FROM {db}.gene WHERE gene_id = {id}".format(
            db=db.db,
            id=gene_id,
        )).description.values[0]
    
    df_plasmids = db.query_data("""
        SELECT * FROM {db}.plasmid
        WHERE plasmid_id IN (
            SELECT plasmid_id FROM {db}.plasmid_gene
            WHERE gene_id = {id}
        )
    """.format(db=db.db, id=gene_id))

    df_files = db.query_data("""
        SELECT * FROM {db}.files
        WHERE file_id IN (
            SELECT file_id FROM {db}.gene_files
            WHERE gene_id = {id}
        )
    """.format(db=db.db, id=gene_id))
    files = df_files.file_name.tolist()
    paths = df_files.path.tolist()
    file_path_pairs = [(f, p) for f, p in zip(files, paths)]

    return render_template(
        "zoom_view.html",
        title="Gene  " + str(gene_id),
        zoom_id=gene_id,
        subtitle=description,
        df_children=None,
        df_parents=df_plasmids.to_html(header="true", index=False, table_id="plasmid_table"),
        file_path_pairs=file_path_pairs,
        upload_form=gene_file_form,
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
