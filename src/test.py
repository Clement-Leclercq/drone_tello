#!/usr/bin/env python3

import sys
import time
import cv2
import imutils
import numpy as np
import sklearn


    # Display barcode and QR code location
def display(img, bbox):
    n = len(bbox)

    pt1 = int(bbox[0][0][0]), int(bbox[0][0][1])    # angle en haut à gauche
    pt2 = int(bbox[0][2][0]), int(bbox[0][2][1])    # angle en bas à droite
    ptCentre = int(bbox[0][0][0]) + int((pt2[0] - pt1[0])/2) , int(bbox[0][0][1]) + int((pt2[1] - pt1[1])/2)
    color = (255, 0, 0)
    print(pt1,pt2,ptCentre)
    cv2.rectangle(img, pt1, pt2, color)
    cv2.circle(img, ptCentre, 2, color, 2)
    # Display results
    cv2.imshow("Results", img)

def main():
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        
        #example code from google TODO: link
        qr_decoder = cv2.QRCodeDetector()
    
        # Detect and decode the qrcode
        data, bbox, rectified_image = qr_decoder.detectAndDecode(frame)
        if len(data)>0:
            print("Decoded Data : {}".format(data))
            display(frame, bbox)
            rectified_image = np.uint8(rectified_image);
            cv2.imshow("Rectified QRCode", rectified_image);
        else:
            print("QR Code not detected")
            cv2.imshow("Results", frame)
        

main()
