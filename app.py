from flask import Flask, request, redirect, render_template_string, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------- ROUTES --------------------

@app.route('/')
def user_view():
    apps = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith('.apk'):
            base = filename[:-4]
            image = base + '.png'
            desc_file = filename + '.txt'
            description = ''
            if os.path.exists(os.path.join(UPLOAD_FOLDER, desc_file)):
                with open(os.path.join(UPLOAD_FOLDER, desc_file)) as f:
                    description = f.read()
            apps.append({
                'name': filename,
                'apk': filename,
                'image': image if os.path.exists(os.path.join(UPLOAD_FOLDER, image)) else '',
                'description': description
            })

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Khali App Store</title>
        <style>
            body { background: #111; color: #eee; font-family: sans-serif; padding: 20px; }
            h1 { color: #0f0; text-align: center; }
            .app { border: 1px solid #444; padding: 15px; margin: 10px 0; border-radius: 8px; background: #1e1e1e; }
            img { max-width: 100px; }
            .desc { margin: 10px 0; }
            a { background: #0f0; padding: 8px 15px; color: #000; border-radius: 5px; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>📱 Khali App Store</h1>
        {% for app in apps %}
            <div class="app">
                <h2>{{ app.name }}</h2>
                {% if app.image %}
                    <img src="/uploads/{{ app.image }}">
                {% endif %}
                <div class="desc">{{ app.description }}</div>
                <a href="/uploads/{{ app.apk }}">Download</a>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, apps=apps)

@app.route('/admin')
def admin_panel():
    apps = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith('.apk'):
            base = filename[:-4]
            desc_file = filename + '.txt'
            description = ''
            if os.path.exists(os.path.join(UPLOAD_FOLDER, desc_file)):
                with open(os.path.join(UPLOAD_FOLDER, desc_file)) as f:
                    description = f.read()
            apps.append({
                'name': filename,
                'filename': filename,
                'description': description
            })

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel</title>
        <style>
            body { background: #111; color: #eee; font-family: sans-serif; padding: 20px; }
            h1 { color: #0f0; text-align: center; }
            form { margin: 20px auto; max-width: 500px; padding: 20px; background: #1e1e1e; border-radius: 10px; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { background: #0f0; color: #000; padding: 10px; width: 100%; }
            .app-list { max-width: 600px; margin: auto; }
            .app-item { background: #222; margin: 10px 0; padding: 15px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>🛠 Admin Panel</h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <label>APK File</label>
            <input type="file" name="apk" required>
            <label>Image (PNG)</label>
            <input type="file" name="image" accept="image/png" required>
            <label>Description</label>
            <textarea name="description" required></textarea>
            <button type="submit">Upload App</button>
        </form>

        <div class="app-list">
            <h2>Uploaded Apps</h2>
            {% for app in apps %}
                <div class="app-item">
                    <strong>{{ app.name }}</strong>
                    <p>{{ app.description }}</p>
                    <form method="POST" action="/delete/{{ app.filename }}">
                        <button type="submit">🗑 Delete</button>
                    </form>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, apps=apps)

@app.route('/upload', methods=['POST'])
def upload():
    apk = request.files['apk']
    image = request.files['image']
    desc = request.form['description']

    apk_path = os.path.join(UPLOAD_FOLDER, apk.filename)
    image_filename = os.path.splitext(apk.filename)[0] + '.png'
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
    desc_path = apk_path + '.txt'

    apk.save(apk_path)
    image.save(image_path)
    with open(desc_path, 'w') as f:
        f.write(desc)

    return redirect('/admin')

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    apk_path = os.path.join(UPLOAD_FOLDER, filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename.replace('.apk', '.png'))
    desc_path = apk_path + '.txt'

    for path in [apk_path, image_path, desc_path]:
        if os.path.exists(path):
            os.remove(path)

    return redirect('/admin')

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# -------------------- RUN APP --------------------
if __name__ == '__main__':
    app.run(debug=True)