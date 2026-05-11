import cv2 as cv
import numpy as np
import os
import json

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

#ЗАДАНИЕ 1
def one():
    img = cv.imread(os.path.join(PROJECT_DIR, 'variant-3.jpeg'))
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    cv.imwrite(os.path.join(PROJECT_DIR, 'task-one-output.jpeg'), hsv_img)


#ЗАДАНИЕ 2 и 3
def two_n_three():
    #МУХА
    fly = cv.imread(os.path.join(PROJECT_DIR, 'fly64.png'), -1)
    b, g, r, fly_mask = cv.split(fly)
    fly_mask_inv = cv.bitwise_not(fly_mask)
    bgr_fly = cv.merge((b, g, r))
    fly_height, fly_width = bgr_fly.shape[:2]
    
    cap = cv.VideoCapture(0)
    cv.namedWindow('PORNO', cv.WINDOW_NORMAL)
    cv.resizeWindow('PORNO', 400, 300)

    cv.createTrackbar('H_min', 'PORNO', 0, 179, lambda x: None)
    cv.createTrackbar('S_min', 'PORNO', 0, 255, lambda x: None)
    cv.createTrackbar('V_min', 'PORNO', 0, 255, lambda x: None)
    cv.createTrackbar('H_max', 'PORNO', 179, 179, lambda x: None)
    cv.createTrackbar('S_max', 'PORNO', 255, 255, lambda x: None)
    cv.createTrackbar('V_max', 'PORNO', 255, 255, lambda x: None)
    cv.createTrackbar('area', 'PORNO', 0, 10000, lambda x: None)

    try:
        with open(os.path.join(PROJECT_DIR, 'params.json'), 'r') as json_file:
            json_data = json.load(json_file)
        cv.setTrackbarPos("H_min", "PORNO", json_data["H_min"])
        cv.setTrackbarPos("S_min", "PORNO", json_data["S_min"])
        cv.setTrackbarPos("V_min", "PORNO", json_data["V_min"])
        cv.setTrackbarPos("H_max", "PORNO", json_data["H_max"])
        cv.setTrackbarPos("S_max", "PORNO", json_data["S_max"])
        cv.setTrackbarPos("V_max", "PORNO", json_data["V_max"])
        cv.setTrackbarPos("area", "PORNO", json_data["area"])
    except:
        json_data = {}

    while True:
        success, img = cap.read()
        if not success:
            break
        
        h_min = cv.getTrackbarPos("H_min", "PORNO")
        s_min = cv.getTrackbarPos("S_min", "PORNO")
        v_min = cv.getTrackbarPos("V_min", "PORNO")
        h_max = cv.getTrackbarPos("H_max", "PORNO")
        s_max = cv.getTrackbarPos("S_max", "PORNO")
        v_max = cv.getTrackbarPos("V_max", "PORNO")
        area_treshold = cv.getTrackbarPos("area", "PORNO")
        
        lower_limit = np.array([h_min, s_min, v_min])
        upper_limit = np.array([h_max, s_max, v_max])

        height, width = img.shape[:2]
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_img, lower_limit, upper_limit)
        mask = cv.medianBlur(mask, 11)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cv.rectangle(img, (width // 2 - 100, height // 2 - 100), (width // 2 + 100, height // 2 + 100), (0, 255, 0), 1)
        
        
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > area_treshold:
                x, y, w, h = cv.boundingRect(cnt)
                rect_color = (0, 255, 0) if x >= width // 2 - 100 and x + w <= width // 2 + 100 and y >= height // 2 - 100 and y + h <= height // 2 + 100 else (0, 0, 255)
                cv.rectangle(img, (x, y), (x + w, y + h), rect_color, 2)
                cv.putText(img, "Apple", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, rect_color, 2)
                #МУХА
                try:
                    x_center, y_center = x + w // 2, y + h // 2
                    roi = img[y_center - fly_height // 2: y_center + fly_height // 2, x_center - fly_width // 2: x_center + fly_width // 2]
                    img_back = cv.bitwise_and(roi, roi, mask=fly_mask_inv)
                    img_front = cv.bitwise_and(bgr_fly, bgr_fly, mask=fly_mask)
                    piece = cv.add(img_back, img_front)
                    img[y_center - fly_height // 2: y_center + fly_height // 2, x_center - fly_width // 2: x_center + fly_width // 2] = piece
                except Exception: #исключение пока было только что муха вылезает за рамки изображения и все крашится
                    pass
                    
        cv.imshow("Original", img)
        cv.imshow("Mask", mask)


        if cv.waitKey(1) & 0xFF == ord('q'):
            json_data["H_min"] = h_min
            json_data["S_min"] = s_min
            json_data["V_min"] = v_min
            json_data["H_max"] = h_max
            json_data["S_max"] = s_max
            json_data["V_max"] = v_max
            json_data["area"] = area_treshold
            with open(os.path.join(PROJECT_DIR, 'params.json'), 'w') as json_file:
                json_data = json.dump(json_data, json_file)
            break

    cap.release()
    cv.destroyAllWindows()


one()
two_n_three()