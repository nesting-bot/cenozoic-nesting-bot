import pyautogui as pg
import pytesseract
import os
import cv2
import numpy as np
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))



pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


def image_processing(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img,(0,0),fx=1,fy=1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.medianBlur(img,5)
    img=cv2.bitwise_not(img)
    (thresh, img) = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return img

def screenshot_for_text(screenshot_region, image_name):
    screenshot = pg.screenshot(region=screenshot_region)
    screenshot.save(image_name + ".png")
    processed_screenshot = image_processing(screenshot)
    return processed_screenshot

def grab_number(image):
    
    def remove_nonnumeric_chars(string):
        output = ''
        
        for char in string:
            if char.isdigit() or char == '-':
                output += char
        # print(output)
        return int(output)
    
    image_text = pytesseract.image_to_string(image, config='--psm 7')
    try:
        return remove_nonnumeric_chars(image_text)
    except Exception:
        return None


def grab_text(image):
    blacklisted_characters = ['\n']
    output = ''
    image_text = pytesseract.image_to_string(image, config='--psm 7')
    for char in image_text:
        if char not in blacklisted_characters:
            output += char
        if char == '@' or char == '©':
            output += ''
    # print(output)
    return output


def read_json():
    with open('data.json', 'r') as f:
        json_data = json.load(f)
    return json_data

def dump_json(data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)