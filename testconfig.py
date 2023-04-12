import cv2;
import pytesseract;

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

name = 'X00016469671.jpg'



def testconfig(name, configtest):

    img = cv2.imread(name)

    #### Text for testing
    #texttest = pytesseract.image_to_string(img)


    ### Cofig
    configname = r' --oem 3 --psm ' + str(configtest) + ' -l eng'

    print('############\nTest: ' + str(configtest))
    ### Box of words
    boxes = pytesseract.image_to_data(img,config=configname)
    #print(boxes)

    class Lines:
        def __init__(self,x,y,w,h,text):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text

    ##Array of detected line
    lineboxes = []



    skip = 0
    for b in boxes.splitlines():
        ## skip header
        if (skip == 0):
            skip = 1
            continue
        ## get box of word in 1 object
        b = b.split()
        #print(b)
        if (len(b) < 12):
            continue


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

        #draw the word-boxes
        cv2.rectangle(img, (x,y) , (w+x,y+h), (0,0,255), 1 )


        #draw the line-boxes
    for l in lineboxes:
        print(l.x, l.y, l.w, l.h, l.text)
        cv2.rectangle(img, (l.x, l.y), (l.w + l.x, l.h + l.y), (255, 0 , 0), 1)

    #print(texttest)
    imgname = 'Result -psm ' + str(configtest)
    cv2.imshow(imgname,img)
    cv2.waitKey(0)


#testconfig(name, 5)

testconfig(name, 1)
testconfig(name, 3)
testconfig(name, 4)
testconfig(name, 6)
testconfig(name, 11)
testconfig(name, 12)



