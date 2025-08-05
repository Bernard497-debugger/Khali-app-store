from flask import Flask, request, jsonify, send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize JSON file if not present
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('.', 'admin.html')

@app.route('/apps')
def get_apps():
    with open(DATA_FILE) as f:
        return jsonify(json.load(f))

@app.route('/upload', methods=['POST'])
def upload_app():
    file = request.files['file']
    icon = request.files['icon']
    name = request.form['name']
    desc = request.form['description']

    file_name = secure_filename(file.filename)
    icon_name = secure_filename(icon.filename)

    file.save(os.path.join(UPLOAD_FOLDER, file_name))
    icon.save(os.path.join(UPLOAD_FOLDER, icon_name))

    with open(DATA_FILE) as f:
        apps = json.load(f)

    apps.append({
        'name': name,
        'description': desc,
        'filename': file_name,
        'icon': icon_name
    })

    with open(DATA_FILE, 'w') as f:
        json.dump(apps, f)

    return redirect('/admin')

@app.route('/delete', methods=['POST'])
def delete_app():
    index = int(request.form['index'])

    with open(DATA_FILE) as f:
        apps = json.load(f)

    if 0 <= index < len(apps):
        # Delete files
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, apps[index]['filename']))
            os.remove(os.path.join(UPLOAD_FOLDER, apps[index]['icon']))
        except:
            pass
        # Remove from list
        apps.pop(index)
        with open(DATA_FILE, 'w') as f:
            json.dump(apps, f)

    return redirect('/')

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)