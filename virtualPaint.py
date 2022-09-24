import cv2
import numpy as np
import screeninfo

cam = cv2.VideoCapture(0)
monitor = screeninfo.get_monitors()
width = monitor[0].width          # Width of screen
height = monitor[0].height         # Height of screen
cam.set(3, width)       # Set width of camera
cam.set(4, height)      # Set height of camera
cam.set(10, 150)        # Set brightness

myColors = [[0,143,224,13,255,255],         #orange  [h_min, s_min, v_min, h_max, s_max, v_max]
          [56,87,61,84,248,255],            #green
          # [15,121,146,48,203,255],        #yellow
          [169,107,0,179,255,255],          #pink
          # [6,91,160,179,160,255]          #skin
          ]

myColorValues = [[51, 153, 255],            #BGR
                 [0,128,0],
                 #[0,255,255],
                 [203,192,255],
                 #[36,85,141]
                ]


def findColor(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for i in range(len(myColors)):
        lower = np.array(myColors[i][:3])
        upper = np.array(myColors[i][3:])
        mask = cv2.inRange(imgHSV,lower,upper)
        x, y = getContours(mask)
        cv2.circle(img, (x,y), 6, myColorValues[i], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,i])
    return newPoints

def getContours(img):
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,w,y,h = 0,0,0,0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area>200:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def drawOnCanvas(points, myColorValues, imgResult):
    for color in range(len(points)):
        for point in range(len(points[color])-1):
            # cv2.circle(imgResult, (point[0],point[1]), 6, myColorValues[point[2]], cv2.FILLED)
            try:
                cv2.line(imgResult,(points[color][point][0],points[color][point][1]),(points[color][point+1][0],points[color][point+1][1]),
                    myColorValues[color],thickness=3)
            except:
                cv2.circle(imgResult, (points[color][point][0],points[color][point][1]), 6, myColorValues[color], cv2.FILLED)


def main():
    points = [[] for i in range(len(myColors))]     #[x, y, colorId]
    while True:
        success, img = cam.read()
        img = cv2.resize(img,(width,height))
        img = cv2.flip(img,1)
        imgResult = np.ones_like(img)*255
        newPoints = findColor(img, myColors)
        if len(newPoints)!=0:
            for newP in newPoints:
                points[newP[2]].append(newP)
                
        if len(points)!=0:
            drawOnCanvas(points, myColorValues, imgResult)
        img = cv2.resize(img, (width//4, height//4))
        cv2.imshow("Virtual Paint", imgResult)
        cv2.imshow("Camera", img)        
        if cv2.waitKey(1) & 0xFF == ord('e'):           # press e for erase.
            points = [[] for i in range(len(myColors))]

        if cv2.waitKey(1) & 0xFF == ord('q'):           # press q for quit.
            break

if __name__ == "__main__":
    main()