import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import io

st.title("QR Code Generator")

# Input fields
data = st.text_input("Enter URL or Text:", "")
filename = st.text_input("Output Filename:", "qr_code.png")
fill_color = st.color_picker("Fill Color", "#000000")
back_color = st.color_picker("Background Color", "#FFFFFF")
logo_file = st.file_uploader("Upload Logo (optional)", type=["png", "jpg", "jpeg"])

if st.button("Generate QR Code"):
    if not data:
        st.error("Please enter URL or text.")
    else:
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

            if logo_file:
                logo = Image.open(logo_file)
                logo_size = min(img.size) // 4
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
                img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

            # Save to buffer
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)

            st.image(buf, caption="Generated QR Code", use_column_width=True)
            st.download_button("Download QR Code", buf, filename=filename, mime="image/png")

            st.success(f"QR code generated successfully!")
        except Exception as e:
            st.error(f"Failed to generate QR code: {str(e)}")
