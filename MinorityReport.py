import cv2
import numpy as np
import pyautogui as pag

def sort_arrays_descending(arrays):
    indices = np.argsort([arr.sum() for arr in arrays])
    descending_indices = indices[::-1]
    sorted_arrays = [arrays[i] for i in descending_indices]
    return sorted_arrays


cam = cv2.VideoCapture(0)
sub_type = 'MOG2'
if sub_type == "MOG2":
    backSub = cv2.createBackgroundSubtractorMOG2(varThreshold=16, detectShadows=False)
    # backSub.setShadowThreshold(0.75)
else:
    backSub = cv2.createBackgroundSubtractorKNN(history=600,dist2Threshold=800, detectShadows=False)

while(cam.isOpened()):

    while True:
        _, frame = cam.read()

        #BACKGROUND SUBTRACTION  + EROSION AND DILTATION
        backSubMask = backSub.apply(frame) 
   
        kernel = np.ones((5, 5), np.uint8) 
  
        img_erosion = cv2.erode(backSubMask, kernel, iterations=1) 
        #img_dilation = cv2.dilate(img_erosion, kernel, iterations=1) 

        #THRESHOLDING
        img_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,img_thresholded = cv2.threshold(img_grayscale,235,255,cv2.THRESH_BINARY)

        #BITWISE
        img_bitwise = cv2.bitwise_and(img_thresholded, img_erosion, mask = None) 

        #CONTOURING
        contours, hierarchy = cv2.findContours(img_bitwise, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours = sort_arrays_descending(contours)

        num_contours = len(contours)
        #print(contours)
        #cv2.drawContours(image = frame, contours = sorted_contours,contourIdx=-1, color=(0,255,0), thickness = 10)
        if(num_contours <= 10):
            cv2.drawContours(frame, sorted_contours, -1, (0,255,0),10,)
        else:
            cv2.drawContours(frame, sorted_contours, 10 , (0,255,0),)
        
        if(num_contours >0):
            pag.moveTo((sorted_contours[0][0][0][0]+sorted_contours[0][1][0][0])/2,(sorted_contours[0][0][0][1]+sorted_contours[0][1][0][1])/2 +50)


        key = cv2.waitKey(1)
        if key == 27:
            break

        cv2.imshow('frame',frame) 
        #cv2.imshow('Background Subtraction Mask', backSubMask) 
        cv2.imshow('Erosion', img_erosion) 
        #cv2.imshow('Dilation', img_dilation) 
        cv2.imshow('Thresholded', img_thresholded)
        cv2.imshow('Bitwise And', img_bitwise)
       
    
    cam.release()
    cv2.destroyAllWindows()
else:
    print("camera is not found")