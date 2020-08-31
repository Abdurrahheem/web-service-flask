import numpy as np
import os
import pandas as pd
from joblib import dump, load
from flask import Flask, request, jsonify, render_template, abort, redirect, url_for, send_file, flash
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

app = Flask(__name__)
knn = load('irismodel.joblib') 

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

def predict(data):
    """ Predicts type of iris flower
    Arguments:
        data: a list of numbers seperated with commas
    Ruturns
        int: predicted class
    """
    data = data.split(',')
    data = [float(s) for s in data]
    result = str(knn.predict(np.array(data).reshape(1,-1)).item(0))
    return result

@app.route('/badrequest400')
def bad_request():
    abort(400)

@app.route('/ind')
def h_world():
    return render_template('index.html')

@app.route('/')
def hello_world():
    print(f'This is {3}')
    return '<h1 style="text-align:center"> Hello, my best frined! <br/> How is the day? </h1>'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f"squared: {escape(float(username)**2)}"

@app.route('/avg/<array>')
def avg(array):
    # avarage of an array
    array = array.split(',')
    array = [float(s) for s in array]
    return f'<h1 style="text-align:center"> The avarage of your array   \
     is {str(sum(array)/len(array))} </h1>'

@app.route('/iris/<data>')
def iris(data):
    data = data.split(',')
    data = [float(s) for s in data]
    result = str(knn.predict(np.array(data).reshape(1,-1)).item(0))
    return '<h2>Your Iris flawer is {}</h2>'.format(result)

@app.route('/show_im')
def show_im():
    # return "<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kosaciec_szczecinkowaty_Iris_setosa.jpg/440px-Kosaciec_szczecinkowaty_Iris_setosa.jpg', alt='Flowers in Chania'>"
    return '<img src="/static/setosa.jpg" alt="setosa">'

@app.route('/iris_post', methods=['POST'])
def iris_post():
    try:
        content = request.get_json()
        content = content['flower']
        rlt = {"class" : predict(content)}
    except:
        return redirect(url_for('bad_request'))
    return jsonify(rlt)

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name.data)
        f = form.file.data
        filename = form.name.data + '.csv'
        # f.save(os.path.join(
        #   filename
        # ))
        upfile = pd.read_csv(f, header=None)
        pd.DataFrame(knn.predict(upfile)).to_csv(filename,index=False)
        return send_file(filename,
                        mimetype='text/csv',
                        attachment_filename=filename,
                        as_attachment=True)
        # return('<h1> File Uploaded </h1>')
    return render_template('submit.html', form=form)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=('GET', 'POST'))
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '<h1> file uploaded </h1>'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''