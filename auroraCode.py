from barcode import EAN13
from barcode.writer import ImageWriter
import time
import random
import os

generated_codes = {}
last_code = 0

def calculate_v(base_code):
    digits = [int(d) for d in str(base_code)]
    total = sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits))
    v = (10 - (total % 10)) % 10
    return v

def create_code(code):
    global last_code
    last_code = code
    digits = [int(d) for d in str(code)]

    if len(digits) not in [4, 5, 6]:
        return
    
    c = "290000" + ("0" * (6 - len(digits)) + str(code))
    c_v = c + str(calculate_v(c))

    result = EAN13(c_v, writer=ImageWriter())
    
    file_path = os.path.join(os.getcwd(), f"{code}_barcode_aurora.png")
    result.save(file_path, text=f"AuroraCode\n{c_v}")

    generated_codes[str(code)] = c_v
    return {"filename": f"{code}_barcode_aurora.png", "path": file_path, "code": str(code), "barcode": c_v}

def generate_random_code():
    next_code = random.randint(1000, 112830)
    create_code(next_code)
