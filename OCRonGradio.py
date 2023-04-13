import gradio as gr
import numpy as np
import testOCR as OCR
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'



def TextLineBox(img):

    class Lines:
        def __init__(self,x,y,w,h,text):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text

    lineboxes = []

    #read image
    #img = cv2.GaussianBlur(img,(1,1),0)


    ### Cofig
    configname = r' --oem 3 --psm ' + str(12) + ' -l eng'

    #### Text for testing
    texttest = pytesseract.image_to_string(img ,config=configname)

    ### Box of words
    boxes = pytesseract.image_to_data(img, config=configname)
    # print(boxes)

    #slit box and concatenate into line
    skip = 0
    for b in boxes.splitlines():
        ## skip header
        if (skip == 0):
            skip = 1
            continue
        ## get box of word in 1 object
        b = b.split()
        if (len(b) < 12):       ## it is a space not a word
            continue

        #print(b)
        x,y,w,h,text = int(b[6]),int(b[7]),int(b[8]),int(b[9]), b[11]


        ### Begin New line if the word having num_word is 1
        if (int(b[5]) == 1):
            lineboxes.append(  Lines(x,y,w,h,text)  )

        ### Next word inline
        else:
            lineboxes[-1].text += ' ' +  text
            if (x > lineboxes[-1].x):
                lineboxes[-1].w = x - lineboxes[-1].x + w
            if (y < lineboxes[-1].y):
                lineboxes[-1].y = y
            if (y+h > lineboxes[-1].y + lineboxes[-1].h):
                lineboxes[-1].h = y+h - lineboxes[-1].y

        #draw the box of WORD
        cv2.rectangle(img, (x,y) , (w+x,y+h), (0,0,255), 1 )


    return texttest,img
    

gr.Interface(fn=OCR.TextLineBox, 
             inputs=gr.Image(),
             outputs=[gr.Text()],
            ).launch()



