# QR Code Generator

A simple QR code generator written in Python with CLI and web-based GUI options.

## Features

- Generate QR codes from text or URLs
- Customize fill and background colors
- Add logos to QR codes
- Command-line interface
- Web-based GUI using Streamlit

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/qr-code-generator.git
   cd qr-code-generator
   ```

2. Create a virtual environment (recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line

```
python main.py "Hello World" -o hello.png -fc blue -bc white
```

Options:
- `-o, --output`: Output filename (default: qr_code.png)
- `-fc, --fill_color`: Fill color (default: black)
- `-bc, --back_color`: Background color (default: white)
- `-l, --logo`: Path to logo image (optional)

### Web GUI (Streamlit)

Run the web-based GUI:
```
streamlit run streamlit_app.py
```

This will open a web interface at http://localhost:8501 where you can:
- Enter text or URL
- Choose colors
- Upload a logo (optional)
- Generate and download QR codes

## Requirements

- Python 3.6+
- qrcode
- pillow
- streamlit
