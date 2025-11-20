from flask import Flask, request, send_file, render_template_string
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import os
import tempfile

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional QR Code Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            margin-top: 50px;
            margin-bottom: 50px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            color: #333;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-label {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        .form-control, .form-control-file {
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            padding: 12px 15px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .btn-generate {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            color: white;
            transition: all 0.3s ease;
            width: 100%;
        }
        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .qr-result {
            text-align: center;
            margin-top: 40px;
        }
        .qr-image {
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin: 20px 0;
        }
        .btn-download {
            background: #28a745;
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-weight: 600;
            color: white;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
            transition: all 0.3s ease;
        }
        .btn-download:hover {
            background: #218838;
            transform: translateY(-1px);
        }
        .feature-icon {
            color: #667eea;
            margin-right: 10px;
        }
        .features {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-top: 40px;
        }
        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-qrcode"></i> Professional QR Code Generator</h1>
            <p>Create custom QR codes with colors and logos instantly</p>
        </div>

        <form method="POST" enctype="multipart/form-data">
            <div class="row">
                <div class="col-md-8">
                    <div class="form-group">
                        <label for="data" class="form-label">
                            <i class="fas fa-link feature-icon"></i>Text or URL
                        </label>
                        <input type="text" class="form-control" id="data" name="data" placeholder="Enter text or URL to encode" required>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="form-group">
                        <label for="fill_color" class="form-label">
                            <i class="fas fa-palette feature-icon"></i>Fill Color
                        </label>
                        <input type="color" class="form-control" id="fill_color" name="fill_color" value="#000000">
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="form-group">
                        <label for="back_color" class="form-label">
                            <i class="fas fa-fill feature-icon"></i>Background
                        </label>
                        <input type="color" class="form-control" id="back_color" name="back_color" value="#ffffff">
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label for="logo" class="form-label">
                    <i class="fas fa-image feature-icon"></i>Logo (Optional)
                </label>
                <input type="file" class="form-control" id="logo" name="logo" accept="image/*">
                <small class="form-text text-muted">Upload a PNG, JPG, or GIF image to embed in the QR code</small>
            </div>

            <button type="submit" class="btn btn-generate">
                <i class="fas fa-magic"></i> Generate QR Code
            </button>
        </form>

        {% if qr_image %}
        <div class="qr-result">
            <h3 class="text-success"><i class="fas fa-check-circle"></i> QR Code Generated Successfully!</h3>
            <img src="{{ qr_image }}" alt="Generated QR Code" class="qr-image img-fluid">
            <br>
            <a href="{{ qr_image }}" class="btn-download" download="qr_code.png">
                <i class="fas fa-download"></i> Download QR Code
            </a>
        </div>
        {% endif %}

        <div class="features">
            <h4 class="text-center mb-4"><i class="fas fa-star"></i> Features</h4>
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-item">
                        <i class="fas fa-palette feature-icon"></i>
                        <span>Custom Colors</span>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <i class="fas fa-image feature-icon"></i>
                        <span>Logo Embedding</span>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <i class="fas fa-download feature-icon"></i>
                        <span>High Quality PNG</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == 'POST':
        data = request.form['data']
        fill_color = request.form['fill_color']
        back_color = request.form['back_color']
        logo_file = request.files.get('logo')

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(image_factory=PilImage, fill_color=fill_color, back_color=back_color)

        if logo_file and logo_file.filename:
            logo = Image.open(logo_file)
            logo_size = min(img.size) // 4
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        img.save(temp_file.name)
        temp_file.close()
        qr_image = f'/qr/{os.path.basename(temp_file.name)}'

        # Store temp file path for serving
        if not hasattr(app, 'temp_files'):
            app.temp_files = []
        app.temp_files.append(temp_file.name)

    return render_template_string(HTML_TEMPLATE, qr_image=qr_image)

@app.route('/qr/<filename>')
def serve_qr(filename):
    temp_dir = tempfile.gettempdir()
    return send_file(os.path.join(temp_dir, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
