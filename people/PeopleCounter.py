import numpy as np
import cv2 as cv
import Person
import time
import pymysql
import urllib.request
import matplotlib.pyplot as plt
import keyboard
from datetime import datetime


date=str(datetime.today().year)+'-'+str(datetime.today().month)+'-'+str(datetime.today().day)
print(date)

try:

    log = open('log.txt', "w")
except:
    print("No se puede abrir el archivo log")
cnt_up = 0
cnt_down = 0
count=0
#cap = cv.VideoCapture('TestVideo.avi')
cap = cv.VideoCapture(1)
#cap=cv.VideoCapture('http://113.198.137.189:8091/?action=stream')
#stream=urllib.request.urlopen('http://192.168.0.35:8091/?action=stream')
cap.set(3,1280)
cap.set(4,1024)
cap.set(15, 0.1)
for i in range(19):
    print(i, cap.get(i))

h = 480
w = 640
frameArea = h * w
areaTH = frameArea / 250
print('Area Threshold', areaTH)

# Lineas de entrada/salida
line_up = int(1.5 * (h / 5))
line_down = int(3.5 * (h / 5))

up_limit = int(.5 * (h / 5))
down_limit = int(4.5* (h / 5))

print("Red line y:", str(line_down))
print("Blue line y:", str(line_up))
line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)
pt1 = [0, line_down];
pt2 = [w, line_down];
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up];
pt4 = [w, line_up];
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit];
pt6 = [w, up_limit];
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit];
pt8 = [w, down_limit];
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))

# Substractor de fondo
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)

# Elementos estructurantes para filtros morfoogicos
kernelOp = np.ones((3, 3), np.uint8)
kernelOp2 = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

# Variables
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

while (cap.isOpened()):
    ret, frame = cap.read()
    for i in persons:
        i.age_one()  # age every person one frame
    #########################
    #   PRE-PROCESAMIENTO   #
    #########################

    # Aplica substraccion de fondo
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    # Binariazcion para eliminar sombras (color gris)
    try:
        ret, imBin = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
        ret, imBin2 = cv.threshold(fgmask2, 200, 255, cv.THRESH_BINARY)
        # Opening (erode->dilate) para quitar ruido.
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        # Closing (dilate -> erode) para juntar regiones blancas.
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print('UP:', cnt_up)
        print('DOWN:', cnt_down)
        break
    #################
    #   CONTORNOS   #
    #################

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    contours0, hierarchy = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt)
        if area > areaTH:
            #################
            #   TRACKING    #
            #################

            # Falta agregar condiciones para multipersonas, salidas y entradas de pantalla.

            M = cv.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv.boundingRect(cnt)

            new = True
            if cy in range(up_limit, down_limit):
                for i in persons:
                    if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                        # el objeto esta cerca de uno que ya se detecto antes
                        new = False
                        i.updateCoords(cx, cy)  # actualiza coordenadas en el objeto and resets age
                        if i.going_UP(line_down, line_up) == True:
                            cnt_up += 1;
                            print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                            log.write("ID: " + str(i.getId()) + ' crossed going up at ' + time.strftime("%c") + '\n')
                        elif i.going_DOWN(line_down, line_up) == True:
                            cnt_down += 1;
                            print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))
                            log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        # sacar i de la lista persons
                        index = persons.index(i)
                        persons.pop(index)
                        del i  # liberar la memoria de i
                if new == True:
                    p = Person.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1
                    #################
            #   DIBUJOS     #
            #################
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv.drawContours(frame, cnt, -1, (0,255,0), 3)

    # END for cnt in contours0

    #########################
    # DIBUJAR TRAYECTORIAS  #
    #########################
    for i in persons:

        cv.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv.LINE_AA)

    #################
    #   IMAGANES    #
    #################
    str_up = 'UP: ' + str(cnt_up)
    str_down = 'DOWN: ' + str(cnt_down)
    frame = cv.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
    frame = cv.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
    frame = cv.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
    frame = cv.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)
    cv.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv.LINE_AA)
    cv.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv.LINE_AA)

    cv.imshow('Frame', frame)
    cv.imshow('Mask', mask)
    print(cnt_up)
   # plt.imshow(frame)
   # plt.show()
    count = count+1
    ##    rawCapture.truncate(0)
    # preisonar ESC para salir
    k = cv.waitKey(30) & 0xff
    if k == 27:


        break
  
  
    if count>100:
        break
    


	


    
# END while(cap.isOpened())

#################
#   LIMPIEZA    #
#################


conn = pymysql.connect(host='localhost', user='ahyun', password='ahyun1000', db='cctv')
try:
	print(1)
	cur=conn.cursor()
	query = "INSERT INTO people_count VALUES(%s,%s,%s,%s,%s)"
	cur.execute(query,(0,377,cnt_up,cnt_down,date))
	conn.commit()
finally:
	cur.close()
	conn.close()


log.flush()
log.close()
cap.release()
cv.destroyAllWindows()



