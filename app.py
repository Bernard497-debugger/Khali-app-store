from flask import Flask, request, render_template_string, redirect, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory storage (MVP, resets when server restarts)
apps = []

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load templates directly
def load_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/')
def index():
    return render_template_string(load_template("index.html"), apps=apps)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global apps
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        file = request.files['file']
        
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            apps.append({
                'name': name,
                'description': desc,
                'filename': file.filename
            })
        return redirect('/admin')
    
    return render_template_string(load_template("admin.html"), apps=apps)

@app.route('/delete/<int:index>')
def delete(index):
    try:
        app_data = apps.pop(index)
        os.remove(os.path.join(UPLOAD_FOLDER, app_data['filename']))
    except:
        pass
    return redirect('/admin')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
