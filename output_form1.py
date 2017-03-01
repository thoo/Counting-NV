from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import SubmitField



class DemoForm(FlaskForm):
    filename = FileField(validators=[FileRequired()])

    submit = SubmitField()
