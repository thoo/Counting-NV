from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import FloatField, validators,SubmitField
from wtforms import SubmitField



class UploadForm(FlaskForm):
    file = FileField(default='image004.npz',validators=[FileRequired(),FileAllowed(['npz'], 'NPZ only!')])
    threshold = FloatField(label='Threshold', default=0.025,validators=[validators.InputRequired()])
    lowerbound = FloatField(label='Lower Limit for NV Radius', default=2.5,validators=[validators.InputRequired()])
    upperbound = FloatField(label='Upper Limit for NV Radius', default=1.0e4,validators=[validators.InputRequired()])
    blur_factor = FloatField(label='Blur Factor for Smoothing', default=0.06,validators=[validators.InputRequired()])
    submit = SubmitField()
