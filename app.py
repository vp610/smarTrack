from flask import Flask, render_template, Response
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
from backend.tracker import mainTracker, VideoDetector

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hiddenkey'
app.config['UPLOAD_FOLDER'] = 'files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def gen(video):
    while True:
        frame = video.get_frame()
        yield (b' --frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/upload", methods=['GET',"POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        file.save(file_path)
        return Response(gen(VideoDetector(file_path)), mimetype='multipart/x-mixed-replace: boundary=frame')
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()