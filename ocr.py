from flask import Flask, request, render_template, redirect, flash
import os
import cv2
import pytesseract
import re

app = Flask(__name__) # creating flask app
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey' # used to manage flash messages 

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\danny\Downloads\tesseract.exe' # path of pytesseract

def extract_text(image_path):
    image = cv2.imread(image_path) # read message using OpenCV
    if image is None: # Checks if there is an image
        return {'OD': {'POWER': 'Error', 'BC': 'Error', 'DIA': 'Error'},
                'OS': {'POWER': 'Error', 'BC': 'Error', 'DIA': 'Error'}}, "Error loading image"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert image to grayscale using OpenCV
    text = pytesseract.image_to_string(gray)  # Extract text from the grayscale image using pytesseract

    pattern = re.compile(r'(OD|OS)\s*([\d\.\-]+)\s*([\d\.\-]+)\s*([\d\.\-]+)', re.IGNORECASE) # Compile a regex pattern to match OD and OS measurements
    matches = pattern.findall(text)  # Find all matches of the pattern in the extracted text

    info = {'OD': {'POWER': '', 'BC': '', 'DIA': ''}, 'OS': {'POWER': '', 'BC': '', 'DIA': ''}} 
    for match in matches: # Iterate over all found matches
        eye, power, bc, dia = match # Extract the details from each match
        info[eye.upper()] = {'POWER': power, 'BC': bc, 'DIA': dia} # Store the details 

    return info, text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            flash("No file selected") # Flash a message if no file was select
            return redirect(request.url) # Redirect the user back to the upload page

        file = request.files['file'] 
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        info, raw_text = extract_text(file_path) # Extract text and information from the uploaded image
        os.remove(file_path)  # Remove the file after processing

        if not any(info['OD'].values()) and not any(info['OS'].values()):  # Check if any information was extracted
            flash("The extracted information is empty. Please upload a higher quality image.")  # Flash a message if no information was found
            return redirect('/')  # Redirect the user back to the upload page

        return render_template('result.html', info=info, raw_text=raw_text)

    return render_template('upload.html') 

if __name__ == '__main__':
    app.run()
