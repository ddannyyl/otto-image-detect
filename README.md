# Otto Prescription Image OCR Feature

This allows users to upload their contact lens prescription and using an OCR library, the information will be extracted and automatically filled in the template of Otto's. This feature reduces the time it takes for users to fill in their prescription information and eliminates the risk of inputting the wrong information

## Getting Started

To run this feature, you need to install the required dependencies and packages.

### 1. Install Dependencies

Run the following command in the powershell
```bash
pip install flask opencv-python pytesseract
```
This installs Flask, a Python web framework used for building the user interface, OpenCV-Python for processing the uploaded images and converting them to grayscale, and Pytesseract, a Python wrapper for Google's Tesseract-OCR engine that extracts text from images.

### 2. Install Packages
Go to the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract) to download the appropriate Tesseract-OCR.

Set the path Tesseract executable path on line 11 of the app.py file:
```bash
pytesseract.pytesseract.tesseract_cmd = r'C:\path\to\tesseract.exe'
```

### 3. Run Program

Run the following command in the powershell
```bash
python ocr.py

```

