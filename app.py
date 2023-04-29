from flask import Flask, send_from_directory, request, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__, static_url_path='', static_folder='smartrack/build')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

@app.route("/", methods=["POST", "GET"])
def handle_form():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        print(file.filename)
        return "File has been uploaded."
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    