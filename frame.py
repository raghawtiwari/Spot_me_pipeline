import cv2
cap= cv2.VideoCapture('/home/raghaw/myfirst/public/test.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite(str(i)+'.jpg',frame)
    i+=1
cap.release()
cv2.destroyAllWindows()
