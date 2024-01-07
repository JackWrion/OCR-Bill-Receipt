import OCR
import os

files = os.listdir('./testcase_source')

# Filter the list to include only text files
image_files = [file for file in files if file.endswith('.jpg')]

# Loop over the text files
check = 0
counter= 0

for img in image_files:
    
    #Process image, them write result and log
    print(counter, "-Processing: " + img)

    #   Below will check special testcase you concern
    # if (img == "X51006619503.jpg"):
    #     check = 1
    # if (check == 0 ):
    #     print("Pass")
    #     continue
    counter = counter + 1
    OCR.OCRText(img)



#### ERROR  ########
#  X51006619503.jpg
#  X51006619506.jpg
#  X51006619782
#  X51006619784.jpg 
#  X51006620182.jpg 
#  X51005719863
# 
# 
# 
# #

