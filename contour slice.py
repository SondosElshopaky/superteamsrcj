import cv2 
import numpy as np 


def keep_printing_contour_area(img):
    # ray_index = ray_index_from_direction("right")
    # lidar_reading = lidar.getRangeImage()[ray_index] * 100
 
    if wall_e_half("right")==True:

        img = camera.getImage()
        img2= camera2.getImage()








        width = camera.getWidth()
        height = camera.getHeight()
        width2 = camera2.getWidth()
        height2 = camera2.getHeight()
        img = np.frombuffer(img, np.uint8).reshape((height, width, 4))  # BGRA format
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Process the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = frame.copy()




        img2 = np.frombuffer(img2, np.uint8).reshape((height2, width2, 4))  # BGRA format
        frame2 = cv2.cvtColor(img2, cv2.COLOR_BGRA2BGR)

        # Process the frame
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        _, thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

        contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)











        if contours or contours2 :
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            print(area)

            print(area)
            print(is_square(largest_contour))

            if area >= 70 and is_square(largest_contour):
                
    


                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)

                # ===== Crop the biggest contour =====
                x, y, w, h = cv2.boundingRect(largest_contour)
                cropped = img[y:y + h, x:x + w]

                # ===== Split into 9 equal parts =====
                cell_h = h // 1
                cell_w = w // 2

                tiles = []
                
                for row in range(1):
                    for col in range(2):
                        x_start = col * cell_w
                        y_start = row * cell_h
                        tile = cropped[y_start:y_start + cell_h, x_start:x_start + cell_w]
                        tiles.append(tile)
                


                # ===== Show all 9 parts and check turquoise =====
                conttourq = []
                for i, tile in enumerate(tiles):
                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)

                    # Define turquoise color range


           

                    # Define dark mask for black corners
                    lower_black1 = np.array([0, 0, 0])
                    upper_black1 = np.array([180, 255, 50])
                    darkmask = cv2.inRange(tile_hsv, lower_black1, upper_black1)

                    turquoise_ratio = cv2.countNonZero(mask) / (tile.shape[0] * tile.shape[1])
                    cv2.imwrite(f"c:/Users/CYBER-TECH/Desktop/saves/Tile {i+1}.png", tile)

                    if turquoise_ratio > 0.3:
                        conttourq.append(True)
                    else:
                        conttourq.append(False)

                print(conttourq)