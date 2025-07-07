import os
import cv2
import imutils
from skimage.metrics import structural_similarity
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_file = request.files['original']
        tampered_file = request.files['tampered']

        if original_file and tampered_file:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)

            original_path = os.path.join(upload_folder, 'original.png')
            tampered_path = os.path.join(upload_folder, 'tampered.png')

            # Resize and save
            original = Image.open(original_file).resize((250, 160))
            tampered = Image.open(tampered_file).resize((250, 160))
            original.save(original_path)
            tampered.save(tampered_path)

            # Read with OpenCV
            original_cv = cv2.imread(original_path)
            tampered_cv = cv2.imread(tampered_path)

            original_gray = cv2.cvtColor(original_cv, cv2.COLOR_BGR2GRAY)
            tampered_gray = cv2.cvtColor(tampered_cv, cv2.COLOR_BGR2GRAY)

            (score, diff) = structural_similarity(original_gray, tampered_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Find differences
            thres = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thres.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(original_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(tampered_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Save result
            result_original = os.path.join(upload_folder, 'marked_original.png')
            result_tampered = os.path.join(upload_folder, 'marked_tampered.png')
            cv2.imwrite(result_original, original_cv)
            cv2.imwrite(result_tampered, tampered_cv)

            return render_template('index.html', score=round(score, 3),
                                   original_image='uploads/marked_original.png',
                                   tampered_image='uploads/marked_tampered.png')

    return render_template('index.html')
