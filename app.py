from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ICON_FOLDER = 'icons'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ICON_FOLDER'] = ICON_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ICON_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "App Store Backend Running!"

@app.route('/upload', methods=['POST'])
def upload():
    apk = request.files['apk']
    icon = request.files['icon']
    name = request.form['name']
    description = request.form['description']

    apk_filename = secure_filename(apk.filename)
    icon_filename = secure_filename(icon.filename)

    apk.save(os.path.join(UPLOAD_FOLDER, apk_filename))
    icon.save(os.path.join(ICON_FOLDER, icon_filename))

    return jsonify({'status': 'success'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/icons/<filename>')
def icon_file(filename):
    return send_from_directory(ICON_FOLDER, filename)

@app.route('/list')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    data = []
    for file in files:
        icon_name = file.replace('.apk', '.png')
        data.append({
            'name': file.replace('.apk', ''),
            'file': file,
            'icon': icon_name,
            'description': ''
        })
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form['filename']
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        icon_filename = filename.replace('.apk', '.png')
        os.remove(os.path.join(ICON_FOLDER, icon_filename))
        return jsonify({'status': 'deleted'})
    except:
        return jsonify({'status': 'error'})

if __name__ == '__main__':
    app.run()
