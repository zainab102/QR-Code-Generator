import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import os

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        # Data input
        layout.addWidget(QLabel("Enter URL or Text:"))
        self.data_entry = QLineEdit()
        layout.addWidget(self.data_entry)

        # Output filename
        layout.addWidget(QLabel("Output Filename:"))
        self.filename_entry = QLineEdit("qr_code.png")
        layout.addWidget(self.filename_entry)

        # Colors
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Fill Color:"))
        self.fill_color_entry = QLineEdit("black")
        color_layout.addWidget(self.fill_color_entry)
        color_layout.addWidget(QLabel("Background Color:"))
        self.back_color_entry = QLineEdit("white")
        color_layout.addWidget(self.back_color_entry)
        layout.addLayout(color_layout)

        # Logo
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(QLabel("Logo Path:"))
        self.logo_entry = QLineEdit()
        logo_layout.addWidget(self.logo_entry)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_logo)
        logo_layout.addWidget(self.browse_button)
        layout.addLayout(logo_layout)

        # Generate button
        self.generate_button = QPushButton("Generate QR Code")
        self.generate_button.clicked.connect(self.generate_qr)
        layout.addWidget(self.generate_button)

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_logo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Image files (*.png *.jpg *.jpeg *.gif)")
        if filename:
            self.logo_entry.setText(filename)

    def generate_qr(self):
        data = self.data_entry.text().strip()
        if not data:
            QMessageBox.warning(self, "Error", "Please enter URL or text.")
            return

        filename = self.filename_entry.text().strip() or "qr_code.png"
        fill_color = self.fill_color_entry.text().strip() or "black"
        back_color = self.back_color_entry.text().strip() or "white"
        logo_path = self.logo_entry.text().strip()

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(image_factory=PilImage, fill_color=fill_color, back_color=back_color)

            if logo_path and os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo_size = min(img.size) // 4
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
                img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

            img.save(filename)
            self.status_label.setText(f"QR code saved as {filename}")
            QMessageBox.information(self, "Success", f"QR code saved as {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR code: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
