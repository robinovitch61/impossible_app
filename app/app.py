import mysql.connector
import os
from src.db_bootstrap import bootstrap
from src.db_helper import MySQLConn
from src.forms import StrainAddForm, StrainDeleteForm, PlasmidAddForm, PlasmidDeleteForm, GeneAddForm, GeneDeleteForm, UploadForm
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import logging
from werkzeug import secure_filename

from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

# upload folder
app.config['UPLOAD_FOLDER'] = './static/assets/uploads'

# secret key for CSRF
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# on app startup
DB_NAME = 'microbes'
bootstrap(DB_NAME)
db = MySQLConn(app, DB_NAME)

# on user visit to landing page
@app.route('/', methods=("GET", "POST"))
def index():

    # add strain
    strain_form = StrainAddForm(request.form)    
    if strain_form.validate_on_submit():
        data = {
            'description': strain_form.description.data,
            'created_by': strain_form.created_by.data,
            'creation_date': strain_form.creation_date.data,
            'notes': strain_form.notes.data,
        }
        db.insert_into_table('strain', data)
        return redirect('/')

    # delete strain
    strain_del_form = StrainDeleteForm(request.form)
    if strain_del_form.validate_on_submit():
        strain_id = strain_del_form.strain_id.data
        db.remove_from_table('strain', 'strain_id = {}'.format(strain_id))
        return redirect('/')

    # add plasmid
    plasmid_form = PlasmidAddForm(request.form)    
    if plasmid_form.validate_on_submit():
        data = {
            '_insert': plasmid_form._insert.data,
            'promoter': plasmid_form.promoter.data,
            'created_by': plasmid_form.created_by.data,
            'creation_date': plasmid_form.creation_date.data,
            'notes': plasmid_form.notes.data,
        }
        db.insert_into_table('plasmid', data)
        return redirect('/')

    # delete plasmid
    plasmid_del_form = PlasmidDeleteForm(request.form)
    if plasmid_del_form.validate_on_submit():
        plasmid_id = plasmid_del_form.plasmid_id.data
        db.remove_from_table('plasmid', 'plasmid_id = {}'.format(plasmid_id))
        return redirect('/')

    # upload files for plasmid
    plasmid_file_form = UploadForm(request.form)
    if plasmid_file_form.validate_on_submit():
        file_names = request.files.getlist(plasmid_file_form.files.name)
        all_files = []
        app.logger.debug(file_names)
        for _file in file_names:
            file_name = secure_filename(_file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            all_files.append(full_path)
            _file.save(full_path)
        app.logger.debug(all_files)
        return redirect('/')
    
    # add gene
    gene_form = GeneAddForm(request.form)
    if gene_form.validate_on_submit():
        data = {
            'description': gene_form.description.data,
            'dna_seq': gene_form.dna_seq.data,
            'created_by': gene_form.created_by.data,
            'creation_date': gene_form.creation_date.data,
            'notes': gene_form.notes.data,
        }
        db.insert_into_table('gene', data)
        return redirect('/')

    # delete gene
    gene_del_form = GeneDeleteForm(request.form)
    if gene_del_form.validate_on_submit():
        gene_id = gene_del_form.gene_id.data
        db.remove_from_table('gene', 'gene_id = {}'.format(gene_id))
        return redirect('/')

    df_strain = db.query_data("SELECT * FROM {db}.strain")
    df_plasmid = db.query_data("SELECT * FROM {db}.plasmid")
    df_gene = db.query_data("SELECT * FROM {db}.gene")
    
    return render_template(
        'index.html',
        strain=df_strain.to_html(classes='data', header="true", index=False),
        plasmid=df_plasmid.to_html(classes='data', header="true", index=False),
        gene=df_gene.to_html(classes='data', header="true", index=False),
        strain_form=strain_form,
        strain_del_form=strain_del_form,
        plasmid_form=plasmid_form,
        plasmid_del_form=plasmid_del_form,
        plasmid_file_form=plasmid_file_form,
        gene_form=gene_form,
        gene_del_form=gene_del_form,
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
