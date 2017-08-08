from output_form1 import UploadForm
from flask import Flask, render_template, request,url_for, redirect
from function  import GDP_PCA_plot
import sys, os, inspect
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import secure_filename


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





@app.route('/', methods=['GET', 'POST'])

def index():

    form = UploadForm()
    filename = 'image005.npz'

    if request.method == 'POST' and form.validate_on_submit():

        # Save uploaded file on server if it exists and is valid
            if file:
                # Make a valid version of filename for any file ystem
                filename = secure_filename(form.file.data.filename)
                form.file.data.save('uploads/' + filename)


                result = GDP_PCA_plot(filename,form.threshold.data,form.lowerbound.data,form.upperbound.data)

    else:
        result =  GDP_PCA_plot(filename,form.threshold.data,form.lowerbound.data,form.upperbound.data,form.blur_factor.data)


    return render_template('view_2_1.html', form=form,
                           result=result)

if __name__ == '__main__':
    app.run(port=33036,debug=True)
