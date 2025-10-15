import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Yüklenen dosyaların kaydedileceği klasör
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB maksimum dosya boyutu

# Dosya uzantısının geçerli olup olmadığını kontrol eden fonksiyon
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ana Sayfa - Fotoğraf Yükleme Formu
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Formda dosya var mı kontrol et
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # Kullanıcı dosya seçmemişse
        if file.filename == '':
            return redirect(request.url)
        # Dosya geçerliyse
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Başarılı yükleme sonrası galeriye yönlendir (isteğe bağlı)
            return redirect(url_for('gallery'))
            
    return render_template('index.html')

# Galeri Sayfası - Yüklenen Fotoğrafları Gösterir
@app.route('/gallery')
def gallery():
    # 'uploads' klasöründeki tüm dosyaları listele
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    # Sadece resim dosyalarını al (gizli dosyaları vs. alma)
    images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('gallery.html', images=images)

# Yüklenen dosyaları sunmak için
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # '0.0.0.0' adresi, aynı ağdaki diğer cihazların erişimine izin verir
    app.run(host='0.0.0.0', port=5000, debug=True)