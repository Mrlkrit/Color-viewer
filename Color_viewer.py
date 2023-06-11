import cv2 as cv
import numpy as np

def track(x):
    pass

cap = cv.VideoCapture(0)


if not cap.isOpened():
    print("Error 420")

if cap.isOpened():
    cv.namedWindow("Video",cv.WINDOW_NORMAL)
    cv.namedWindow("Trackbar",cv.WINDOW_NORMAL)
    cv.namedWindow("Processed",cv.WINDOW_NORMAL)
    # Create HSV tracbars
    cv.createTrackbar("H_min", "Trackbar" , 0, 180, track)
    cv.createTrackbar("H_max", "Trackbar" , 180, 180, track)
    cv.createTrackbar("S_min", "Trackbar" , 0, 255, track)
    cv.createTrackbar("S_max", "Trackbar" , 255, 255, track)
    cv.createTrackbar("V_min", "Trackbar" , 0, 255, track)
    cv.createTrackbar("V_max", "Trackbar" , 255, 255, track)
    cv.createTrackbar("Obj_size", "Trackbar" , 0, 255, track)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv.imshow('Video', frame)

            h_min = cv.getTrackbarPos("H_min", "Trackbar")
            h_max = cv.getTrackbarPos("H_max", "Trackbar")
            s_min = cv.getTrackbarPos("S_min", "Trackbar")
            s_max = cv.getTrackbarPos("S_max", "Trackbar")
            v_min = cv.getTrackbarPos("V_min", "Trackbar")
            v_max = cv.getTrackbarPos("V_max", "Trackbar")
            obj_size = cv.getTrackbarPos("Obj_size", "Trackbar")

            low = np.array([h_min, s_min, v_min])
            up = np.array([h_max, s_max, v_max])

            # Processing
            frame = cv.GaussianBlur(frame, (5,5), 1)

            frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            frame = cv.inRange(frame, low, up)
            # delete objects smaller than given size, count 8 pixel neighbours
            blob_amount, frame, stats, centroids = cv.connectedComponentsWithStats(frame, 8)
            sizes = stats[1:, -1]; 
            blob_amount = blob_amount - 1
            image = np.zeros((frame.shape))
            for i in range(0, blob_amount):
                if sizes[i] >= obj_size:
                    image[frame == i + 1] = 255

            # Display result
            cv.imshow("Processed", image)
        # Close when "p" pressed
        if cv.waitKey(1) & 0xFF == ord('p'):
            break
        
cap.release()
cv.destroyAllWindows()
