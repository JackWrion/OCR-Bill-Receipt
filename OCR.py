import cv2
import pytesseract
import numpy as np
from thefuzz import fuzz
import os

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def OCRText(name):

    class Lines:
        def __init__(self,x,y,w,h,text):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text

    ##Array of detected line
    lineboxes = []

    dir_source = ".\\testcase_source"
    file_path = os.path.join(dir_source, name)


    #read image
    img = cv2.imread(file_path)
    img_iou = img        ## Using later
    img = cv2.GaussianBlur(img,(3,3),0)
    

    #### Text for testing
    #texttest = pytesseract.image_to_string(img)

    ### Cofig
    configname = r' --oem 3 --psm ' + str(12) + ' -l eng'


    ### contain all date about Box of words
    boxes = pytesseract.image_to_data(img, config=configname)
    
    #print(boxes)

    linetest = []
    iou = []
    textmatching = []

    #slit box and concatenate into line
    skipheader = 0              #skip header
    skipfirstline = 0           #skip firstline traceback

    ################################################
    #---------- Detect and draw detected line_box  
    ################################################

    name_test = name.replace('.jpg','_test.txt')
    name_test_dir = os.path.join(".\\result", name_test)
    with open(name_test_dir, mode='w', encoding='utf-8') as file:

        for b in boxes.splitlines():
            ## skip header
            if (skipheader == 0):
                skipheader = 1
                continue

            ## get box of word in 1 object
            b = b.split()
            if (len(b) < 12):       ## it is a space not a word
                continue

            #print(b)
            x,y,w,h,text = int(b[6]),int(b[7]),int(b[8]),int(b[9]), b[11]


            ### Begin New line if the word having num_word is 1, and done previus line
            if (int(b[5]) == 1):
                if (skipfirstline == 0):        # cant done prev line, cuz its the first line
                    skipfirstline = 1       
                else:                           # if newline then done previous line, and done
                    l = lineboxes[-1]        
                    combine_str = str(l.x) + ','+ str(l.y) + ','+ \
                        str(l.x+l.w) + ','+ str(l.y) + ','+ \
                        str(l.x+l.w) + ','+ str(l.y+l.h) +','+ \
                        str(l.x) + ','+ str(l.y+l.h) + ',' + \
                        l.text + '\n'
                    file.write(combine_str)

                    line = combine_str.split(',',8)
                    linetest.append(line)

                    #draw Box of Line as RED box
                    #print(l.x, l.y, l.w, l.h, l.text)
                    cv2.rectangle(img, (l.x, l.y), (l.w + l.x, l.h + l.y), (255, 0 , 0), 1)
                    #file.close

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


        ## Draw the last line
        
        # if (len(lineboxes) == 0):
        #     print ("!! NOT DONE: " + name)
        #     return
        
        try:
            l = lineboxes[-1]
        except:
            print ("!!!---CAN NOT DETECTED: " + name)
        else:        
            combine_str = str(l.x) + ','+ str(l.y) + ','+ \
                str(l.x+l.w) + ','+ str(l.y) + ','+ \
                str(l.x+l.w) + ','+ str(l.y+l.h) +','+ \
                str(l.x) + ','+ str(l.y+l.h) + ',' + \
                l.text + '\n'
            file.write(combine_str)

            line = combine_str.split(',',8)
            linetest.append(line)

            #print(l.x, l.y, l.w, l.h, l.text)
            cv2.rectangle(img, (l.x, l.y), (l.w + l.x, l.h + l.y), (255, 0 , 0), 1)


            #draw the box of WORD
            #cv2.rectangle(img, (x,y) , (w+x,y+h), (0,0,255), 1 )


    #linesample = []
    

    ################################################
    ##          Read, draw grouth_truth      #######
    ##          Calc IOU, draw IOU           #######
    ##          Write log file               #######
    ################################################
    #img_iou = cv2.imread(file_path)

    ## Read grouth_truth file
    name_sample = name.replace('.jpg', '.txt')
    dir_name_sample = os.path.join(".\\testcase_source", name_sample)

    ## Write log file
    checkname = name.replace('.jpg', '_log.txt')
    dir_checkname = os.path.join(".\\log", checkname)
    checklogfile = open(  dir_checkname, "w"  )

    with open(dir_name_sample, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.split(',',8)
            #linesample.append(line)
            ground_truth = []
            ground_truth.extend([ int(line[0]), int(line[1]), int(line[4]), int(line[5])   ])
            
            check = 0

            for lt in linetest:
                test = []
                test.extend([int(lt[0]), int(lt[1]), int(lt[4]), int(lt[5])])
                temp_iou = get_iou(ground_truth,test,img_iou)
                if temp_iou > 0.4:
                    iou.append(temp_iou)
                    textmatching.append( fuzz.ratio(line[-1].lower(), lt[-1].lower()) )
                    checklogfile.write(   "iou: " +  str(temp_iou) +'    '+ "txt: " +  str(textmatching[-1]) +'\n'+ line[-1] + lt[-1] + '\n')
                    # print(textmatching[-1])
                    # print(line[-1].lower())
                    # print(lt[-1].lower())
                    check = 1
                    break
                else:
                    pass

            if check == 0:                  ## the line that cannot detect
                ### check ERROR: the lines aren't detected
                #-------#print("error: " + line[-1])
                #########
                checklogfile.write( "!-Error: " + line[-1] + '\n')
                iou.append(0)


            cv2.rectangle(img, (int(line[0]), int(line[1])), (int(line[4]), int(line[5])), (0,0,255), 1)


        if (len(textmatching) == 0):
            matchingpercent = 0
        else: 
            matchingpercent = sum(textmatching)/len(textmatching)
        
        if (len(iou) == 0):
            average = 0
        else: 
            average = sum(iou) / len(iou)*100

        
        #print(textmatching)
        checklogfile.write('Average IOU:  ' + name +'   '+ str(average) + '\n')
        checklogfile.write('Text Matching % :  ' + name +'   '+ str(matchingpercent) + '\n')

        # print('Average IOU:  ' + name +'   '+ str(average))
        # print('Text Matching % :  ' + name +'   '+ str(matchingpercent))

    checklogfile.close()

    

    img_test = name.replace(".jpg","_test.jpg")
    img_test = os.path.join(".\\result", img_test) 
    cv2.imwrite(img_test, img)
    img_test = img_test.replace("_test.jpg","_iou.jpg")
    cv2.imwrite(img_test, img_iou)
    print("Done: " + name)
###################  DONE  ######################################################



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

    if (iou > 0.4):
        cv2.rectangle(img, (ix1, iy1), (ix2, iy2), (255, 0, 255), 1)

    return iou


# name = 'X51006620182.jpg'
# OCRText(name)



