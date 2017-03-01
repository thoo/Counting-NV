from flask import url_for, redirect, render_template
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename
from flask import Flask, render_template, request
import sys, os, inspect
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import secure_filename

class UploadForm(Form):
    file = FileField()
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.update(dict(
    SECRET_KEY = 'pandindan lan',
    CSRF_ENABLED = True,
))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return redirect(url_for('upload'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(port=33035,debug=True)
