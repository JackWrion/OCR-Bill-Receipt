import testOCR

import os

files = os.listdir('./')

# Filter the list to include only text files
image_files = [file for file in files if file.endswith('.jpg')]

# Loop over the text files
for img in image_files:
    # Open the file for reading
    print(img)
    testOCR.OCRImage(img)


