from output_form1 import DemoForm
from flask import Flask, render_template, request,url_for, redirect
from function  import GDP_PCA_plot
import sys, os, inspect
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import FloatField, validators,SubmitField

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.update(dict(
    SECRET_KEY = 'pandindan lan',
    CSRF_ENABLED = True,
))


# Relative path of directory for uploaded files
UPLOAD_DIR = 'uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)



# Allowed file types for file upload
ALLOWED_EXTENSIONS = set([ 'npz'])

def allowed_file(filename):
    """Does filename have the right extension?"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class UploadForm(FlaskForm):
    file = FileField(default='image004.npz',validators=[FileRequired(),FileAllowed(['npz'], 'NPZ only!')])
    threshold = FloatField(label='Threshold', default=0.025,validators=[validators.InputRequired()])
    lowerbound = FloatField(label='Lower Limit for NV diameter', default=0.0,validators=[validators.InputRequired()])
    upperbound = FloatField(label='Upper Limit for NV diameter', default=1.0e10,validators=[validators.InputRequired()])
    submit = SubmitField()



@app.route('/checknv', methods=['GET', 'POST'])

def index():

    form = UploadForm()
    #filename = None

    if request.method == 'POST' and form.validate_on_submit():

        # Save uploaded file on server if it exists and is valid
            if file:
                # Make a valid version of filename for any file ystem
                filename = secure_filename(form.file.data.filename)
                form.file.data.save('uploads/' + filename)

                print(filename)
                print(form.threshold.data)

                result = GDP_PCA_plot(filename,form.threshold.data,form.lowerbound.data,form.upperbound.data)
                #return redirect(url_for('index'))
                #return redirect(url_for('checknv'))
    else:
        result = None


    return render_template('view_2_1.html', form=form,
                           result=result)

if __name__ == '__main__':
    app.run(port=33035,debug=True)
