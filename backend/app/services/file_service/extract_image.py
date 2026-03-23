from pathlib import Path

import pytesseract
from PIL import Image


def extract_image(path: Path) -> str:
    image = Image.open(str(path))
    return pytesseract.image_to_string(image)
