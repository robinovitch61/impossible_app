from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
import sys

class StrainAddForm(FlaskForm):
    strain_id = StringField('ID (optional, will overwrite):')
    description = StringField('Description:', validators=[DataRequired()])
    created_by = StringField('Created By:', validators=[DataRequired()])
    creation_date = DateField('Date:', validators=[DataRequired(message="YYYY-MM-DD")])
    notes = StringField('Notes (optional):')
    plasmid_ids = StringField('Plasmid IDs (optional), e.g. 1, 12, 14:')
    submit = SubmitField('Add')

class StrainDeleteForm(FlaskForm):
    strain_del_id = StringField('Strain ID To Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class PlasmidAddForm(FlaskForm):
    plasmid_id = StringField('ID (optional, will overwrite):')
    insert = StringField('Insert:', validators=[DataRequired()])
    promoter = StringField('Promoter:', validators=[DataRequired()])
    created_by = StringField('Created By:', validators=[DataRequired()])
    creation_date = DateField('Date:', validators=[DataRequired()])
    notes = StringField('Notes:')
    gene_ids = StringField('Gene IDs (optional), e.g. 1, 12, 14:')
    submit = SubmitField('Add')

class PlasmidDeleteForm(FlaskForm):
    plasmid_del_id = StringField('Plasmid ID To Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class GeneAddForm(FlaskForm):
    gene_id = StringField('ID (optional, will overwrite):')
    description = StringField('Description:', validators=[DataRequired()])
    dna_seq = StringField('DNA Sequence:', validators=[DataRequired()])
    created_by = StringField('Created By:', validators=[DataRequired()])
    creation_date = DateField('Date:', validators=[DataRequired()])
    notes = StringField('Notes:')
    submit = SubmitField('Add')

class GeneDeleteForm(FlaskForm):
    gene_id = StringField('Gene ID To Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class UploadForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Upload')
