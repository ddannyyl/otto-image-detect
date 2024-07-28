from flask import Flask, request, render_template, redirect, flash
import os
import cv2
import pytesseract
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey'

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\danny\Downloads\tesseract.exe'

def extract_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {'OD': {'POWER': 'Error', 'BC': 'Error', 'DIA': 'Error'},
                'OS': {'POWER': 'Error', 'BC': 'Error', 'DIA': 'Error'}}, "Error loading image"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    pattern = re.compile(r'(OD|OS)\s*([\d\.\-]+)\s*([\d\.\-]+)\s*([\d\.\-]+)', re.IGNORECASE)
    matches = pattern.findall(text)

    info = {'OD': {'POWER': '', 'BC': '', 'DIA': ''}, 'OS': {'POWER': '', 'BC': '', 'DIA': ''}}
    for match in matches:
        eye, power, bc, dia = match
        info[eye.upper()] = {'POWER': power, 'BC': bc, 'DIA': dia}

    return info, text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            flash("No file selected")
            return redirect(request.url)

        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        info, raw_text = extract_text(file_path)
        os.remove(file_path)

        if not any(info['OD'].values()) and not any(info['OS'].values()):
            flash("The extracted information is empty. Please upload a higher quality image.")
            return redirect('/')

        return render_template('result.html', info=info, raw_text=raw_text)

    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
