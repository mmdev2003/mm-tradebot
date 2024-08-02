from io import BytesIO
from pdf2image import convert_from_bytes
import pdfkit
import imgkit

def convert_html_to_png(html_str):
    options = {
        'quality': '100',
        'encoding': "UTF-8",
        "format": 'png',
        'enable-local-file-access': ''
    }
    
    html_data = imgkit.from_string(html_str, output_path=None, options=options)
    return html_data
