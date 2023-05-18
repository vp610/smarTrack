from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
from backend.tracker import mainTracker

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hiddenkey'
app.config['UPLOAD_FOLDER'] = 'files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route("/", methods=['GET',"POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        file.save(file_path)

        return "Number of packages: " + mainTracker(file_path)
    return render_template('index.html', form=form)

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run()
    
>>>>>>> 04c72fdbd8bce429c65303dcee41d22237c16474
