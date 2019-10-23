#!/usr/bin/env python3
#! to install any lib you need to add --user at the end of any cmd
import sys
import math 
import socket
import selectors
import traceback
import time
import libclient
import socket
import imutils
import numpy as np
import cv2
import numpy.ma as ma
from functools import reduce
import objects as objects
from skimage.measure import centroid

# Capture video from file

old_frame = cv2.VideoCapture(0)
#old_frame = cv2.VideoCapture("C:\\Users\\Intern.DESKTOP-KOT5JSA\\source\\repos\\PythonApplication1\\VidTest.avi")


width = int(old_frame.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(old_frame.get(cv2.CAP_PROP_FRAME_HEIGHT ))
hote = "192.168.1.240"  # The server's hostname or IP address
port = 8080  # The port used by the server
TILT = 980
INIT = 0
D = 2
Dmm = 1500

debug = False
isSocketSending = True
TEST = INIT + TILT

# Definition objet a suivre
#eponge
#objectWidth= 100
#objectHeight = 80
#objectPrecision = 40
#Drone
objectWidth= 120
objectHeight = 80
objectPrecision = 40

if isSocketSending:
    s = socket.socket()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((hote, port))
    print 
    "Connection on {}".format(port)
   
#Matrice video
diff = np.ndarray(shape=(height, width))

# Compteur de commandes send
compteurTILTPANN = 0
X = 640 / 2
Y = 480 / 2
XP = 640 // 2
YP = 480 // 2
while True:
    
    
    ret, frame = old_frame.read()
    
    diff = cv2.resize(diff, (640, 480))

    Pan = 0
    Til = 0
    if ret == True:
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (640, 480))

        diff_frame = gray - diff
        #Cherchant le min
        diff_frame -= diff_frame.min()
        #cherchant le max
        disp_frame = np.uint8(255.0*diff_frame/float(diff_frame.max()))
        #Un masque qui filtre les pixel negatif
        disp_frame = ma.masked_array(disp_frame, mask=(disp_frame > 0))
        final=disp_frame-gray
        
        
        cv2.imshow('diff_frame',diff)
        #fin de parcour de la matrice
        #diff old frame
        diff = gray
        #old_frame = gray

        thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnts = imutils.grab_contours(cnts)
        


        # loop over the contours
        for c in cnts:
            

            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            if (w < objectWidth-objectPrecision or w > objectWidth + objectPrecision 
                or h < objectHeight - objectPrecision or h > objectHeight + objectPrecision):
                continue
            Frame1=cv2.rectangle(diff, (x, y), (x + w, y + h), (199, 153, 200), 1)
            #cv2.circle(Frame1, (x, y), 6, (255, 255, 255), 1)
            cv2.putText(Frame1, "DRONE", (x - 20, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            H,W=Frame1.shape[:2]
            X = x + W // 2
            Y = y + H // 2
            #Frame=cv2.rectangle(diff_frame, (x, y), (x + w, y + h), (199, 153, 200), 1)


            # initialize our centroid tracker and frame dimensions


            # calculate the center of the frame as this is where we will
            # try to keep the object







            #print('Centre de gravite, Position drone (X,Y):')
            # find object location
            objectLoc = (Frame1, (X, Y))

            # draw both the ID of the object and the centroid of the
            # object on the output frame

            # loop over the tracked objects

            #cX = int(M["m10"] / M["m00"])
            #cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            #cv2.drawContours(Frame,objectLoc, -1, (0, 255, 0), 2)

            #cv2.imshow("Image", Frame)

            # update our centroid tracker using the computed set of bounding
            # box rectangles



           # print('X:', X)
           # print('Y:', Y)
            
               # print('location:', objectLoc)

            

            #tgO = (Y - (H // 2) ) // D 
            #tgO = ((y-YP)/D * 1.37/1000)
            #tgO = (y-YP)/(Dmm*0.5)
            tgO = (y-180)/(Dmm*0.5)

            #tgX = (X - (W // 2) ) // D
            #tgX = ((x-XP)/D* 1.37/1000)
            #tgX = (x-XP)/(Dmm*0.5)
            tgX = x/(Dmm*0.5) 

            Tilt = np.arctan(tgO)
            
               # print('Tilt in radian', Tilt)

            Pann = np.arctan(tgX)
            
               # print('Pann in radian', Pann)
           
            
            TILT = np.degrees(Tilt)
            TILT = TILT * 100
           # print('TILT in degrees', TILT)
            
            PANN = np.degrees(Pann)
            PANN = PANN * 100
          #  print('PANN in degrees', PANN)
            if debug:
                print ("x=",x," y=",y)
                print('TgO=', tgO," : tgX=",tgX," : atanO=",Tilt," : atanX=",Pann)
           
            
            # print('PANN in centi-degrees', str(np.around(PANN)) + "00")
            # print('TILT in centi-degrees', str(np.around(TILT)) + "00")
            Pan = int(np.around(PANN))
            Til = int(np.around(TILT))

        #print ("Pan=",Pan," Til=",Til)
        
        if (Pan < 1000):
            if (Pan > 0):
                PANN = "PANN:"+"00" + str(Pan)
            elif (Pan > -1000):
                PANN = "PANN:"+"-0" + str(Pan*-1)
            else:
                PANN = "PANN:" + str(Pan)
        elif (Pan < 10000):
            PANN = "PANN:"+"0" + str(Pan)
        elif (Pan >= 10000):
            PANN = "PANN:"+ str(Pan)
        
        if (Til < 1000):
            if (Til > 0):
                TILT = "TILT:"+"00"+ str(Til)
            elif (Til > -1000):
                TILT = "TILT:"+"-0"+ str(Til*-1)
            else:
                TILT = "TILT:"+ str(Til)
        elif (Til < 10000):
            TILT = "TILT:"+"0"+ str(Til)
        else:
            TILT = "TILT:"+ str(Til)
        
        if isSocketSending:
            socket.send(TILT.encode())
            compteurTILTPANN = compteurTILTPANN +1
        #  print('Moving  TILT')
        time.sleep(0.3)
       # print('Sleep')
        if isSocketSending:
            socket.send(PANN.encode())
            compteurTILTPANN = compteurTILTPANN +1
     #   print('Moving  PANN')  
        
            
        XVecteruDiff =  X - XP
        YVecteurDiff = Y - YP
        XVecteruDiff =  0
        YVecteurDiff = 0

        if (XVecteruDiff != 0) | (YVecteurDiff != 0) :
            if isSocketSending:
                socket.send(TILT.encode())
                time.sleep(0.6)
       #     print('Sending your TILT')
                socket.send(PANN.encode())
                compteurTILTPANN = compteurTILTPANN +1
         #   print('Sending your PANN')  
        print ("[",compteurTILTPANN,"]","P:",PANN,":T:",TILT)
        XP = X
        YP = Y
         
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
      #  print('END!')
        break





old_frame.release()
cv2.destroyAllWindows()






print 
"Close"
if IsConnected:
    socket.close()
sel = selectors.DefaultSelector()


def create_request(action, value):
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    if IsConnected:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(sel, sock, addr, request)
        sel.register(sock, events, data=message)


if len(sys.argv) != 8:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
request = create_request(action, value)
start_connection(host, port, request)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
