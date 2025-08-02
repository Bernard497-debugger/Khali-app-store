from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB limit

apps_data = []

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def user():
    return render_template('user.html', apps=apps_data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        apk = request.files['apk']
        icon = request.files['icon']

        apk_filename = secure_filename(apk.filename)
        icon_filename = secure_filename(icon.filename)

        apk_path = os.path.join(app.config['UPLOAD_FOLDER'], apk_filename)
        icon_path = os.path.join(app.config['UPLOAD_FOLDER'], icon_filename)

        apk.save(apk_path)
        icon.save(icon_path)

        app_info = {
            'id': len(apps_data),
            'title': title,
            'description': description,
            'category': category,
            'apk': apk_filename,
            'icon': icon_filename
        }

        apps_data.append(app_info)
        return redirect(url_for('admin'))

    return render_template('admin.html', apps=apps_data)

@app.route('/delete/<int:app_id>', methods=['POST'])
def delete(app_id):
    global apps_data
    apps_data = [app for app in apps_data if app['id'] != app_id]
    return redirect(url_for('admin'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)