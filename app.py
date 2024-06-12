import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'uploads/'
STATIC_FOLDER = 'static/qr_codes/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        urls = request.form['urls']
        urls_list = urls.split()
        
        # Validation des URLs
        if not urls_list:
            flash("Please enter at least one URL.")
            return redirect(url_for('generate'))
        
        urls_string = "\n".join(urls_list)
        img = qrcode.make(urls_string)
        file_path = os.path.join(app.config['STATIC_FOLDER'], 'myqr.png')
        img.save(file_path)
        flash("QR Code generated successfully!")
        return render_template('generate.html', qr_code_url=url_for('static', filename='qr_codes/myqr.png'))
    return render_template('generate.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode_qr():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            decoded_data = decode(Image.open(file_path))
            if decoded_data:
                result = decoded_data[0].data.decode('ascii')
                flash("QR Code decoded successfully!")
                return render_template('decode.html', decoded_text=result)
            else:
                flash("Could not decode the QR Code.")
                return render_template('decode.html')
    return render_template('decode.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
