import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


### This will return LINE_BOXES ARRAY
def TextLineBox(name, configtest):

    class Lines:
        def __init__(self,x,y,w,h,text):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text

    ##Array of detected line
    lineboxes = []


    #read image
    img = cv2.imread(name)
    img = cv2.GaussianBlur(img,(3,3),0)

    #### Text for testing
    #texttest = pytesseract.image_to_string(img)


    ### Cofig
    configname = r' --oem 3 --psm ' + str(configtest) + ' -l eng'

    print('############\nTest: ' + str(configtest))


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
        #cv2.rectangle(img, (x,y) , (w+x,y+h), (0,0,255), 1 )

    #cv2.imshow('Boxes ', img)
    #cv2.waitKey(0)
    return  lineboxes



#### this will DRAW lineboxes and WRITE to file
def WriteToFile(name,lineboxes,img):

    #img = cv2.imread(name)
    #write to file text
    name = name.replace('.jpg','')
    name = name + 'test.txt'
    with open(name, mode='w', encoding='utf-8') as file:

        for l in lineboxes:
            combine_str = str(l.x) + ','+ str(l.y) + ','+ \
                  str(l.x+l.w) + ','+ str(l.y) + ','+ \
                  str(l.x+l.w) + ','+ str(l.y+l.h) +','+ \
                  str(l.x) + ','+ str(l.y+l.h) + ',' + \
                  l.text + '\n'
            file.write(combine_str)

            #draw Box of Line
            print(l.x, l.y, l.w, l.h, l.text)
            cv2.rectangle(img, (l.x, l.y), (l.w + l.x, l.h + l.y), (255, 0 , 0), 1)

    #print(texttest)

    #result = 'Result Test ' + str(name)
    #cv2.imshow(result,img)
    #cv2.waitKey(0)


# this will DRAW LINE BOXES based on GROUND_TRUTH
def SampleOCR(name,img):
    #img = cv2.imread(name)

    name = name.replace('.jpg', '.txt')

    with open(name, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.split(',')
            cv2.rectangle(img, (int(line[0]), int(line[1])), (int(line[4]), int(line[5])), (0,0,255), 1)

    result = 'Result Sample ' + str(name)
    cv2.imshow(result, img)
    cv2.waitKey(0)


def get_iou(ground_truth, pred, img):
    # coordinates of the area of intersection.
    ix1 = np.maximum(ground_truth[0], pred[0])
    iy1 = np.maximum(ground_truth[1], pred[1])
    ix2 = np.minimum(ground_truth[2], pred[2])
    iy2 = np.minimum(ground_truth[3], pred[3])

    # Intersection height and width.
    i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
    i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))

    area_of_intersection = i_height * i_width

    # Ground Truth dimensions.
    gt_height = ground_truth[3] - ground_truth[1] + 1
    gt_width = ground_truth[2] - ground_truth[0] + 1

    # Prediction dimensions.
    pd_height = pred[3] - pred[1] + 1
    pd_width = pred[2] - pred[0] + 1

    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection

    iou = area_of_intersection / area_of_union

    if (iou > 0.5):
        cv2.rectangle(img, (ix1, iy1), (ix2, iy2), (255, 100, 100), 1)


    return iou


def AverageIOU(name):
    img = cv2.imread(name)
    namesample = name.replace('.jpg', '.txt')
    nametest = name.replace('.jpg', 'test.txt')

    linesample = []
    linetest = []

    with open(namesample, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.split(',')
            linesample.append(line)

    with open(nametest, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.split(',')
            linetest.append(line)

    iou = []

    for ls in linesample:
        ground_truth = []
        ground_truth.extend([ int(ls[0]), int(ls[1]), int(ls[4]), int(ls[5])         ])

        check = 0

        for lt in linetest:
            test = []
            test.extend([int(lt[0]), int(lt[1]), int(lt[4]), int(lt[5])])
            temp_iou = get_iou(ground_truth,test,img)
            if temp_iou > 0.5:
                iou.append(temp_iou)
                check = 1
                break
            else:
                pass

        if check == 0:
            iou.append(0)


    cv2.imshow("IOU", img)
    cv2.waitKey(0)
    average = sum(iou) / len(iou)
    print('Average IOU:  ' + str(average))





name = 'X51005230657.jpg'


#lineboxes = TextLineBox(name, 6)
#WriteToFile(name, lineboxes)

img = cv2.imread(name)

lineboxes = TextLineBox(name, 12)
WriteToFile(name, lineboxes,img)
SampleOCR(name,img)

AverageIOU(name)





