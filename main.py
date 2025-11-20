import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import argparse
import os

def generate_qr_code(data, filename="qr_code.png", fill_color="black", back_color="white", logo_path=None):
    """
    Generate a QR code with optional customization.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo_size = min(img.size) // 4
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

    img.save(filename)
    print(f"QR code saved as {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes from text or URL.")
    parser.add_argument("data", nargs='?', help="The text or URL to encode in the QR code.")
    parser.add_argument("-o", "--output", default="qr_code.png", help="Output filename (default: qr_code.png)")
    parser.add_argument("-fc", "--fill_color", default="black", help="Fill color for QR code (default: black)")
    parser.add_argument("-bc", "--back_color", default="white", help="Background color for QR code (default: white)")
    parser.add_argument("-l", "--logo", help="Path to logo image to embed in QR code")
    parser.add_argument("-b", "--batch", help="Path to file containing multiple data entries (one per line)")

    args = parser.parse_args()

    if args.batch:
        if not os.path.exists(args.batch):
            print(f"Batch file {args.batch} not found.")
            return
        with open(args.batch, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            data = line.strip()
            if data:
                filename = f"qr_{i+1}.png"
                generate_qr_code(data, filename, args.fill_color, args.back_color, args.logo)
                print(f"Generated QR for: {data}")
    else:
        if not args.data:
            parser.error("data is required unless using --batch")
        generate_qr_code(args.data, args.output, args.fill_color, args.back_color, args.logo)

if __name__ == "__main__":
    main()
