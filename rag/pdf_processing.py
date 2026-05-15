import fitz
import pytesseract

from PIL import Image

import sys

if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    

def procesar_pdf(pdf_path):

    texto_completo = ""

    fue_ocr = False

    doc = fitz.open(pdf_path)

    for page in doc:

        texto = page.get_text()

        # =====================================
        # SI NO HAY TEXTO → OCR
        # =====================================

        if not texto.strip():

            fue_ocr = True

            pix = page.get_pixmap()

            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            texto = pytesseract.image_to_string(
                img,
                lang="spa"
            )

        texto_completo += texto + "\n"

    doc.close()

    return texto_completo, fue_ocr