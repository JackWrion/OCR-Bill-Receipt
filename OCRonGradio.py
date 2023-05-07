import gradio as gr
import tempfile
import cv2
import pytesseract
from fastapi import FastAPI

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
    img = cv2.GaussianBlur(img,(3,3),0)


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
        cv2.rectangle(img, (x,y) , (w+x,y+h), (255,0,0), 2 )


    return texttest,img
    

def Download(text):
    with open("test.txt", "w") as file:
        file.write(text)
    return "test.txt"






    
# mainInterface = gr.Interface(fn=TextLineBox, 
#              inputs=gr.Image(),
#              outputs=[gr.Text(label="Result Text"), gr.Image(label="Boxes of Line")],
#             )



with gr.Blocks (theme='JohnSmith9982/small_and_pretty'  , css="#SUBMIT {background-color: red} #DOWNLOAD {background-color: green}") as demo:
    with gr.Row():
        with gr.Column():
            input = gr.Image()
            text_output = gr.Text(label="Result Text")
            file_output = gr.File()
            with gr.Row():
                submit_btn = gr.Button("SUBMIT" , elem_id="SUBMIT")
                download_btn = gr.Button("DOWNLOAD", elem_id="DOWNLOAD")
                clear_btn = gr.Button("CLEAR")

        with gr.Column():
            image_output = gr.Image()

    submit_btn.click(TextLineBox, input, outputs= [text_output, image_output, ] )
    download_btn.click(Download, text_output, outputs= file_output )
    clear_btn.click(lambda: [None,None,None], inputs=None, outputs= [text_output, file_output, image_output])




app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/" )
