from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class StrainAddForm(FlaskForm):
    description = StringField('Description:', validators=[DataRequired()])
    created_by = StringField('Created By:', validators=[DataRequired()])
    creation_date = DateField('Date:', validators=[DataRequired()])
    notes = StringField('Notes:')
    submit = SubmitField('Add Strain')

class StrainDeleteForm(FlaskForm):
    strain_id = StringField('Strain ID To Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete Strain')

class PlasmidAddForm(FlaskForm):
    insert = StringField('Insert:', validators=[DataRequired()])
    promoter = StringField('Promoter:', validators=[DataRequired()])
    created_by = StringField('Created By:', validators=[DataRequired()])
    creation_date = DateField('Date:', validators=[DataRequired()])
    notes = StringField('Notes:')
    submit = SubmitField('Add Plasmid')

class PlasmidDeleteForm(FlaskForm):
    plasmid_id = StringField('Plasmid ID To Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete Plasmid')

class GeneAddForm(FlaskForm):
    description = StringField('Description:', validators=[DataRequired()])
    dna_seq = StringField('DNA Sequence:', validators=[DataRequired()])
    created_by = StringField('Created By:', validators=[DataRequired()])
    creation_date = DateField('Date:', validators=[DataRequired()])
    notes = StringField('Notes:')
    submit = SubmitField('Add Gene')

class GeneDeleteForm(FlaskForm):
    gene_id = StringField('Gene ID To Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete Gene')