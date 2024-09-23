import fitz
import cv2
import numpy as np
import pytesseract
from PIL import Image
import os

# Specify the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(np.array(img))
    return images

def correct_orientation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    angle = rect[2]
    if angle < -45:
        angle = 90 + angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def preprocess_image(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    denoised = cv2.fastNlMeansDenoising(gray)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def extract_table(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(img, [c], -1, (0,0,255), 2)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(img, [c], -1, (0,0,255), 2)

    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 100
    max_area = 5000
    table_cells = [cv2.boundingRect(c) for c in cnts if min_area < cv2.contourArea(c) < max_area]
    table_cells = sorted(table_cells, key=lambda x: (x[1], x[0]))

    return img, table_cells

def ocr_table(image, cells):
    results = []
    for cell in cells:
        x, y, w, h = cell
        roi = image[y:y+h, x:x+w]
        custom_config = r'--oem 3 --psm 6 -l eng+kan'
        text = pytesseract.image_to_string(roi, config=custom_config)
        results.append(text.strip())
    return results

def process_pdf(pdf_path):
    images = extract_images_from_pdf(pdf_path)
    
    for page_num, image in enumerate(images):
        print(f"Processing page {page_num + 1}")
        
        # Correct orientation
        corrected_image = correct_orientation(image)
        
        # Preprocess
        preprocessed_image = preprocess_image(corrected_image)
        
        # Save preprocessed image
        temp_image_path = f'temp_page_{page_num}.png'
        cv2.imwrite(temp_image_path, preprocessed_image)
        
        # Extract table and OCR
        img, cells = extract_table(temp_image_path)
        ocr_results = ocr_table(img, cells)

        print(f"Results for page {page_num + 1}:")
        for idx, text in enumerate(ocr_results):
            print(f"Cell {idx + 1}: {text}")
        
        # Remove temporary image file
        os.remove(temp_image_path)

# Main execution
if __name__ == "__main__":
    pdf_path = 'primary-english.pdf'
    process_pdf(pdf_path)