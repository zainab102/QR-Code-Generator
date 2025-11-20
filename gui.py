import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x500")

        # Data input
        tk.Label(root, text="Enter URL or Text:").pack(pady=10)
        self.data_entry = tk.Entry(root, width=50)
        self.data_entry.pack(pady=5)

        # Output filename
        tk.Label(root, text="Output Filename:").pack(pady=10)
        self.filename_entry = tk.Entry(root, width=50)
        self.filename_entry.insert(0, "qr_code.png")
        self.filename_entry.pack(pady=5)

        # Colors
        tk.Label(root, text="Fill Color:").pack(pady=5)
        self.fill_color_entry = tk.Entry(root, width=20)
        self.fill_color_entry.insert(0, "black")
        self.fill_color_entry.pack(pady=5)

        tk.Label(root, text="Background Color:").pack(pady=5)
        self.back_color_entry = tk.Entry(root, width=20)
        self.back_color_entry.insert(0, "white")
        self.back_color_entry.pack(pady=5)

        # Logo
        tk.Label(root, text="Logo Path (optional):").pack(pady=5)
        self.logo_frame = tk.Frame(root)
        self.logo_frame.pack(pady=5)
        self.logo_entry = tk.Entry(self.logo_frame, width=30)
        self.logo_entry.pack(side=tk.LEFT)
        tk.Button(self.logo_frame, text="Browse", command=self.browse_logo).pack(side=tk.RIGHT)

        # Generate button
        tk.Button(root, text="Generate QR Code", command=self.generate_qr).pack(pady=20)

        # Status
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

    def browse_logo(self):
        filename = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if filename:
            self.logo_entry.delete(0, tk.END)
            self.logo_entry.insert(0, filename)

    def generate_qr(self):
        data = self.data_entry.get().strip()
        if not data:
            messagebox.showerror("Error", "Please enter URL or text.")
            return

        filename = self.filename_entry.get().strip() or "qr_code.png"
        fill_color = self.fill_color_entry.get().strip() or "black"
        back_color = self.back_color_entry.get().strip() or "white"
        logo_path = self.logo_entry.get().strip()

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
            self.status_label.config(text=f"QR code saved as {filename}")
            messagebox.showinfo("Success", f"QR code saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
