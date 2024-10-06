from flask import Flask, abort, render_template, redirect, url_for, flash, request
import os
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
#import pandas as pd
from colorstats import get_image_top_colors

#from dotenv import load_dotenv
#load_dotenv()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

UPLOAD_FOLDER = '/static/assets/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('image_stats', filename=filename))
        else:
            flash('File type not allowed')
            return redirect(request.url)             

    path = f"{os.getcwd()}/{app.config['UPLOAD_FOLDER']}"
    existing_files = os.listdir(path )
    return render_template("index.html", uploads = existing_files)
    

@app.route('/image_stats/<string:filename>', methods=['GET','POST'])
def image_stats(filename):
    path = f"{os.getcwd()}/{app.config['UPLOAD_FOLDER']}"
    img_stats = get_image_top_colors(path , filename,2000)    
    
    top_color_stats = [(k, v) for k, v in img_stats["colors"].items()]

    return render_template("show-image-stats.html", stats = img_stats["stats"], top_colors = top_color_stats, file = filename  )


if __name__ == '__main__':
    app.run(debug=True)
