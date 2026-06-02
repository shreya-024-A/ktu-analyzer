import pytesseract
from PIL import Image

def calculate_points(category, level):
    # Mapping based on Page 3-5 of your PDF
    points_table = {
        'Sports': {'I': 8, 'II': 15, 'III': 25, 'IV': 40, 'V': 60},
        'Cultural': {'I': 8, 'II': 12, 'III': 20, 'IV': 40, 'V': 60},
        'NSS': 60,
        'NCC': 60,
        'MOOC': 50,
    }
    
    if category in ['NSS', 'NCC', 'MOOC']:
        return points_table.get(category, 0)
    
    return points_table.get(category, {}).get(level, 0)

def verify_name(file_path, user_full_name):
    try:
        # Requires Tesseract installed on system
        text = pytesseract.image_to_string(Image.open(file_path))
        return user_full_name.lower() in text.lower()
    except:
        return False