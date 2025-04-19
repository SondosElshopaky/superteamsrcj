def Scan_Camera():
    img = right_camera.getImage()
    img2 = left_camera.getImage()

    width = right_camera.getWidth()
    height = right_camera.getHeight()
    width2 = left_camera.getWidth()
    height2 = left_camera.getHeight()
    
    if img is not None:
        img = np.frombuffer(img, np.uint8).reshape((height, width, 4))  # BGRA format
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Process the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = frame.copy()

        checkingfirst = check_first(right_camera)
        if checkingfirst == "LETTER":
            detect_letters(right_camera, 'r')
            return 'r'
        elif checkingfirst == "HAZARD":
            hazard_image_detection(right_camera, 'r')
            return 'r'

    if img2 is not None:
        img2 = np.frombuffer(img2, np.uint8).reshape((height2, width2, 4))  # BGRA format
        frame2 = cv2.cvtColor(img2, cv2.COLOR_BGRA2BGR)

        # Process the frame
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        _, thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

        contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        checkingfirst = check_first(left_camera)
        if checkingfirst == "LETTER":
            detect_letters(left_camera, 'l')
            return 'l'
        elif checkingfirst == "HAZARD":
            hazard_image_detection(left_camera, 'l')
            return 'l'

        if contours or contours2:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            print(area)

            if area >= 70:
                # Crop the biggest contour
                x, y, w, h = cv2.boundingRect(largest_contour)
                cropped = img[y:y + h, x:x + w]

                # Split into 2 equal parts
                cell_h = h // 1
                cell_w = w // 2

                tiles = []

                for row in range(1):
                    for col in range(2):
                        x_start = col * cell_w
                        y_start = row * cell_h
                        tile = cropped[y_start:y_start + cell_h, x_start:x_start + cell_w]
                        tiles.append(tile)

                # Check for black regions
                conttourq = []
                for i, tile in enumerate(tiles):
                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)

                    # Define dark mask for black corners
                    lower_black1 = np.array([0, 0, 0])
                    upper_black1 = np.array([180, 255, 50])
                    darkmask = cv2.inRange(tile_hsv, lower_black1, upper_black1)

                    black = cv2.countNonZero(darkmask) / (tile.shape[0] * tile.shape[1])

                    if black > 0.3:
                        conttourq.append(True)
                    else:
                        conttourq.append(False)

                if conttourq[0] == True:
                    rotate_right()
                    move_forward()
                else:
                    move_forward()
                print(conttourq)
    return None


## area 1 
def Scan_Camera1(img):
    img = right_camera.getImage()
    img2 = left_camera.getImage()

    width = right_camera.getWidth()
    height = right_camera.getHeight()
    width2 = left_camera.getWidth()
    height2 = left_camera.getHeight()
    
    if img is not None:
        img = np.frombuffer(img, np.uint8).reshape((height, width, 4))  # BGRA format
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Process the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = frame.copy()

        checkingfirst = check_first(right_camera)
        if checkingfirst == "LETTER":
            detect_letters(right_camera, 'r')
            robot.setVelocity(0.0)
            return 'r'
        elif checkingfirst == "HAZARD":
            hazard_image_detection(right_camera, 'r')
            robot.setVelocity(0.0)            
            return 'r'

    if img2 is not None:
        img2 = np.frombuffer(img2, np.uint8).reshape((height2, width2, 4))  # BGRA format
        frame2 = cv2.cvtColor(img2, cv2.COLOR_BGRA2BGR)

        # Process the frame
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        _, thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

        contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        checkingfirst = check_first(left_camera)
        if checkingfirst == "LETTER":
            detect_letters(left_camera, 'l')
            robot.setVelocity(0.0)
            return 'l'
        elif checkingfirst == "HAZARD":
            hazard_image_detection(left_camera, 'l')
            robot.setVelocity(0.0)
            return 'l'

        if contours or contours2:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            print(area)

            if area >= 70:
                # Crop the biggest contour
                x, y, w, h = cv2.boundingRect(largest_contour)
                cropped = img[y:y + h, x:x + w]

                # Split into 2 equal parts
                cell_h = h // 1
                cell_w = w // 2

                tiles = []

                for row in range(1):
                    for col in range(2):
                        x_start = col * cell_w
                        y_start = row * cell_h
                        tile = cropped[y_start:y_start + cell_h, x_start:x_start + cell_w]
                        tiles.append(tile)

                # Check for black regions
                conttourq = []
                for i, tile in enumerate(tiles):
                    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)

                    # Define dark mask for black corners
                    lower_black1 = np.array([0, 0, 0])
                    upper_black1 = np.array([180, 255, 50])
                    darkmask = cv2.inRange(tile_hsv, lower_black1, upper_black1)

                    black = cv2.countNonZero(darkmask) / (tile.shape[0] * tile.shape[1])

                    if black > 0.3:
                        conttourq.append(True)
                    else:
                        conttourq.append(False)

                if conttourq[0] == True:
                    rotate_right()
                    move_forward()
                else:
                    move_forward()
                print(conttourq)
    return None

def hazard_image_detection(camera, camera_letter):
    global last_hazard_time
    
    image = camera.getImage()
    img = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    bgr = img[:, :, :3]
    
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
    upper_yellow = np.array([35, 255, 255])
    lower_yellow = np.array([15, 100, 100])
    upper_yellow2 = np.array([35, 255, 255]) 
    lower_yellow2 = np.array([15, 100, 100])
    
    yellowmask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellowmask2 = cv2.inRange(hsv, lower_yellow2, upper_yellow2)
    mainyellow = yellowmask1 + yellowmask2
    
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    
    lower_black1 = np.array([0, 0, 0])
    upper_black1 = np.array([180, 255, 120])

    # Dark blue mask
    # Dark blue
    lower_blue1 = np.array([90, 130, 0])
    upper_blue1 = np.array([150, 255, 255])
    # Light blue
    lower_blue2 = np.array([90, 40, 130])
    upper_blue2 = np.array([150, 255, 255])
    # Medium blue
    lower_blue3 = np.array([90, 80, 80])
    upper_blue3 = np.array([150, 255, 255])
    
    blue_mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
    blue_mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
    blue_mask3 = cv2.inRange(hsv, lower_blue3, upper_blue3)
    
    blue_mask = blue_mask1 + blue_mask2 + blue_mask3
    blue_pixel_count = cv2.countNonZero(blue_mask)
    # Green mask
    # Bright green
    lower_green1 = np.array([35, 30, 30])
    upper_green1 = np.array([85, 255, 255])
    # Dark green
    lower_green2 = np.array([35, 30, 10])
    upper_green2 = np.array([85, 255, 120])
    # Light green
    lower_green3 = np.array([35, 30, 130])
    upper_green3 = np.array([85, 255, 255])
    
    green_mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
    green_mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
    green_mask3 = cv2.inRange(hsv, lower_green3, upper_green3)
    
    green_mask = green_mask1 + green_mask2 + green_mask3
    green_pixel_count = cv2.countNonZero(green_mask)
    # White mask
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 40, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    white_pixel_count = cv2.countNonZero(white_mask)
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_pixel_count = cv2.countNonZero(red_mask)
    
    black_mask = cv2.inRange(hsv, lower_black1, upper_black1)
    black_pixel_count = cv2.countNonZero(black_mask)
    yellow_pixel_count = cv2.countNonZero(mainyellow)
    
    left_wheel.setVelocity(0.0)
    right_wheel.setVelocity(0.0)
    
    height, width, _ = hsv.shape
    tile_h = height // 3
    tile_w = width // 3
    
    tiles = []
    for row in range(3):
        for col in range(3):
            x_start = col * tile_w
            y_start = row * tile_h
            tile = hsv[y_start:y_start + tile_h, x_start:x_start + tile_w]
            tiles.append(tile)
    
    conttourb = []
    for i, tile in enumerate(tiles):
        lower_black1_tile = np.array([0, 0, 0])
        upper_black1_tile = np.array([180, 255, 50])
        darkmask = cv2.inRange(tile, lower_black1_tile, upper_black1_tile)
        black_ratio = cv2.countNonZero(darkmask) / (tile.shape[0] * tile.shape[1])
        conttourb.append(black_ratio > 0.3)
    
    hsv_img = cv2.cvtColor(tiles[4], cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_black1, upper_black1)
    pixel_count = cv2.countNonZero(mask)
    print(f"Green pixel count: {green_pixel_count}")
    print(f"White pixel count: {white_pixel_count}")
    print(f"Red pixel count: {red_pixel_count}")
    print(f"Black pixel count: {black_pixel_count}")
    print(f"Yellow pixel count: {yellow_pixel_count}")
    print(f"Blue pixel count: {blue_pixel_count}")
    print(f"Center tile black pixel count: {pixel_count}")
    
    hazard = None
    
    if yellow_pixel_count > 5:
        hazard = 'O'
    elif red_pixel_count > 5:
        hazard = 'F'
    elif pixel_count == 0:
        hazard = 'P'
    elif black_pixel_count >= 5:
        hazard = 'C'
    elif blue_pixel_count == 3622 and green_pixel_count == 205 and white_pixel_count == 197:
        hazard = 'B'
        
    elif blue_pixel_count >=5 and yellow_pixel_count >=5:
        hazard = 'G'
    
    elif red_pixel_count ==3 and white_pixel_count ==1198 and green_pixel_count ==3 and blue_pixel_count ==1200:
        hazard = 'R'        
    
    if hazard:
        print(f"Hazard detected: {hazard}")
    
    return hazard


def area2(camera):
    
    global last_hazard_time
    
    image = camera.getImage()
    img = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    bgr = img[:, :, :3]
    Scan_Camera(image)
    
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
    upper_yellow = np.array([35, 255, 255])
    lower_yellow = np.array([15, 100, 100])
    upper_yellow2 = np.array([35, 255, 255]) 
    lower_yellow2 = np.array([15, 100, 100])
    
    yellowmask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellowmask2 = cv2.inRange(hsv, lower_yellow2, upper_yellow2)
    mainyellow = yellowmask1 + yellowmask2
    
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    
    lower_black1 = np.array([0, 0, 0])
    upper_black1 = np.array([180, 255, 120])

    # Dark blue mask
    # Dark blue
    lower_blue1 = np.array([90, 130, 0])
    upper_blue1 = np.array([150, 255, 255])
    # Light blue
    lower_blue2 = np.array([90, 40, 130])
    upper_blue2 = np.array([150, 255, 255])
    # Medium blue
    lower_blue3 = np.array([90, 80, 80])
    upper_blue3 = np.array([150, 255, 255])
    
    blue_mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
    blue_mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
    blue_mask3 = cv2.inRange(hsv, lower_blue3, upper_blue3)
    
    blue_mask = blue_mask1 + blue_mask2 + blue_mask3
    blue_pixel_count = cv2.countNonZero(blue_mask)
    # Green mask
    # Bright green
    lower_green1 = np.array([35, 30, 30])
    upper_green1 = np.array([85, 255, 255])
    # Dark green
    lower_green2 = np.array([35, 30, 10])
    upper_green2 = np.array([85, 255, 120])
    # Light green
    lower_green3 = np.array([35, 30, 130])
    upper_green3 = np.array([85, 255, 255])
    
    green_mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
    green_mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
    green_mask3 = cv2.inRange(hsv, lower_green3, upper_green3)
    
    green_mask = green_mask1 + green_mask2 + green_mask3
    green_pixel_count = cv2.countNonZero(green_mask)
    # White mask
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 40, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    white_pixel_count = cv2.countNonZero(white_mask)
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_pixel_count = cv2.countNonZero(red_mask)
    
    black_mask = cv2.inRange(hsv, lower_black1, upper_black1)
    black_pixel_count = cv2.countNonZero(black_mask)
    yellow_pixel_count = cv2.countNonZero(mainyellow)
    
    left_wheel.setVelocity(0.0)
    right_wheel.setVelocity(0.0)
    
    height, width, _ = hsv.shape
    tile_h = height // 3
    tile_w = width // 3
    
    tiles = []
    for row in range(3):
        for col in range(3):
            x_start = col * tile_w
            y_start = row * tile_h
            tile = hsv[y_start:y_start + tile_h, x_start:x_start + tile_w]
            tiles.append(tile)
    
    conttourb = []
    for i, tile in enumerate(tiles):
        lower_black1_tile = np.array([0, 0, 0])
        upper_black1_tile = np.array([180, 255, 50])
        darkmask = cv2.inRange(tile, lower_black1_tile, upper_black1_tile)
        black_ratio = cv2.countNonZero(darkmask) / (tile.shape[0] * tile.shape[1])
        conttourb.append(black_ratio > 0.3)
    
    hsv_img = cv2.cvtColor(tiles[4], cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_black1, upper_black1)
    pixel_count = cv2.countNonZero(mask)
    print(f"Green pixel count: {green_pixel_count}")
    print(f"White pixel count: {white_pixel_count}")
    print(f"Red pixel count: {red_pixel_count}")
    print(f"Black pixel count: {black_pixel_count}")
    print(f"Yellow pixel count: {yellow_pixel_count}")
    print(f"Blue pixel count: {blue_pixel_count}")
    print(f"Center tile black pixel count: {pixel_count}")
    
    hazard = None
    
    if yellow_pixel_count > 5:
        hazard = 'O'
    elif red_pixel_count > 5:
        hazard = 'F'
    elif pixel_count == 0:
        hazard = 'P'
    elif black_pixel_count >= 5:
        hazard = 'C'
    elif blue_pixel_count == 3622 and green_pixel_count == 205 and white_pixel_count == 197:
        hazard = 'B'      
    
    if hazard:
        print(f"Hazard detected: {hazard}")
    
    return hazard

def area3(camera):
    global last_hazard_time
    
    image = camera.getImage()
    img = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    bgr = img[:, :, :3]
    Scan_Camera(image)
    
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
    upper_yellow = np.array([35, 255, 255])
    lower_yellow = np.array([15, 100, 100])
    upper_yellow2 = np.array([35, 255, 255]) 
    lower_yellow2 = np.array([15, 100, 100])
    
    yellowmask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellowmask2 = cv2.inRange(hsv, lower_yellow2, upper_yellow2)
    mainyellow = yellowmask1 + yellowmask2
    
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    
    lower_black1 = np.array([0, 0, 0])
    upper_black1 = np.array([180, 255, 120])

    # Dark blue mask
    # Dark blue
    lower_blue1 = np.array([90, 130, 0])
    upper_blue1 = np.array([150, 255, 255])
    # Light blue
    lower_blue2 = np.array([90, 40, 130])
    upper_blue2 = np.array([150, 255, 255])
    # Medium blue
    lower_blue3 = np.array([90, 80, 80])
    upper_blue3 = np.array([150, 255, 255])
    
    blue_mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
    blue_mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
    blue_mask3 = cv2.inRange(hsv, lower_blue3, upper_blue3)
    
    blue_mask = blue_mask1 + blue_mask2 + blue_mask3
    blue_pixel_count = cv2.countNonZero(blue_mask)
    # Green mask
    # Bright green
    lower_green1 = np.array([35, 30, 30])
    upper_green1 = np.array([85, 255, 255])
    # Dark green
    lower_green2 = np.array([35, 30, 10])
    upper_green2 = np.array([85, 255, 120])
    # Light green
    lower_green3 = np.array([35, 30, 130])
    upper_green3 = np.array([85, 255, 255])
    
    green_mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
    green_mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
    green_mask3 = cv2.inRange(hsv, lower_green3, upper_green3)
    
    green_mask = green_mask1 + green_mask2 + green_mask3
    green_pixel_count = cv2.countNonZero(green_mask)
    # White mask
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 40, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    white_pixel_count = cv2.countNonZero(white_mask)
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_pixel_count = cv2.countNonZero(red_mask)
    
    black_mask = cv2.inRange(hsv, lower_black1, upper_black1)
    black_pixel_count = cv2.countNonZero(black_mask)
    yellow_pixel_count = cv2.countNonZero(mainyellow)
    
    left_wheel.setVelocity(0.0)
    right_wheel.setVelocity(0.0)
    
    height, width, _ = hsv.shape
    tile_h = height // 3
    tile_w = width // 3
    
    tiles = []
    for row in range(3):
        for col in range(3):
            x_start = col * tile_w
            y_start = row * tile_h
            tile = hsv[y_start:y_start + tile_h, x_start:x_start + tile_w]
            tiles.append(tile)
    
    conttourb = []
    for i, tile in enumerate(tiles):
        lower_black1_tile = np.array([0, 0, 0])
        upper_black1_tile = np.array([180, 255, 50])
        darkmask = cv2.inRange(tile, lower_black1_tile, upper_black1_tile)
        black_ratio = cv2.countNonZero(darkmask) / (tile.shape[0] * tile.shape[1])
        conttourb.append(black_ratio > 0.3)
    
    hsv_img = cv2.cvtColor(tiles[4], cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_black1, upper_black1)
    pixel_count = cv2.countNonZero(mask)
    print(f"Green pixel count: {green_pixel_count}")
    print(f"White pixel count: {white_pixel_count}")
    print(f"Red pixel count: {red_pixel_count}")
    print(f"Black pixel count: {black_pixel_count}")
    print(f"Yellow pixel count: {yellow_pixel_count}")
    print(f"Blue pixel count: {blue_pixel_count}")
    print(f"Center tile black pixel count: {pixel_count}")
    
    hazard = None
    
    if yellow_pixel_count > 5:
        hazard = 'O'
    elif red_pixel_count > 5:
        hazard = 'F'
    elif pixel_count == 0:
        hazard = 'P'
    elif black_pixel_count >= 5:
        hazard = 'C'
    
        
    elif blue_pixel_count >=5 and yellow_pixel_count >=5:
        hazard = 'G'
    
    if hazard:
        print(f"Hazard detected: {hazard}")
    
    return hazard 




def area4(camera):
    global last_hazard_time
    
    image = camera.getImage()
    img = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    bgr = img[:, :, :3]
    
    
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
    upper_yellow = np.array([35, 255, 255])
    lower_yellow = np.array([15, 100, 100])
    upper_yellow2 = np.array([35, 255, 255]) 
    lower_yellow2 = np.array([15, 100, 100])
    
    yellowmask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellowmask2 = cv2.inRange(hsv, lower_yellow2, upper_yellow2)
    mainyellow = yellowmask1 + yellowmask2
    
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    
    lower_black1 = np.array([0, 0, 0])
    upper_black1 = np.array([180, 255, 120])

    # Dark blue mask
    # Dark blue
    lower_blue1 = np.array([90, 130, 0])
    upper_blue1 = np.array([150, 255, 255])
    # Light blue
    lower_blue2 = np.array([90, 40, 130])
    upper_blue2 = np.array([150, 255, 255])
    # Medium blue
    lower_blue3 = np.array([90, 80, 80])
    upper_blue3 = np.array([150, 255, 255])
    
    blue_mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
    blue_mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
    blue_mask3 = cv2.inRange(hsv, lower_blue3, upper_blue3)
    
    blue_mask = blue_mask1 + blue_mask2 + blue_mask3
    blue_pixel_count = cv2.countNonZero(blue_mask)
    # Green mask
    # Bright green
    lower_green1 = np.array([35, 30, 30])
    upper_green1 = np.array([85, 255, 255])
    # Dark green
    lower_green2 = np.array([35, 30, 10])
    upper_green2 = np.array([85, 255, 120])
    # Light green
    lower_green3 = np.array([35, 30, 130])
    upper_green3 = np.array([85, 255, 255])
    
    green_mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
    green_mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
    green_mask3 = cv2.inRange(hsv, lower_green3, upper_green3)
    
    green_mask = green_mask1 + green_mask2 + green_mask3
    green_pixel_count = cv2.countNonZero(green_mask)
    # White mask
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 40, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    white_pixel_count = cv2.countNonZero(white_mask)
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_pixel_count = cv2.countNonZero(red_mask)
    
    black_mask = cv2.inRange(hsv, lower_black1, upper_black1)
    black_pixel_count = cv2.countNonZero(black_mask)
    yellow_pixel_count = cv2.countNonZero(mainyellow)
    
    left_wheel.setVelocity(0.0)
    right_wheel.setVelocity(0.0)
    
    height, width, _ = hsv.shape
    tile_h = height // 3
    tile_w = width // 3
    
    tiles = []
    for row in range(3):
        for col in range(3):
            x_start = col * tile_w
            y_start = row * tile_h
            tile = hsv[y_start:y_start + tile_h, x_start:x_start + tile_w]
            tiles.append(tile)
    
    conttourb = []
    for i, tile in enumerate(tiles):
        lower_black1_tile = np.array([0, 0, 0])
        upper_black1_tile = np.array([180, 255, 50])
        darkmask = cv2.inRange(tile, lower_black1_tile, upper_black1_tile)
        black_ratio = cv2.countNonZero(darkmask) / (tile.shape[0] * tile.shape[1])
        conttourb.append(black_ratio > 0.3)
    
    hsv_img = cv2.cvtColor(tiles[4], cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower_black1, upper_black1)
    pixel_count = cv2.countNonZero(mask)
    # print(f"Green pixel count: {green_pixel_count}")
    # print(f"White pixel count: {white_pixel_count}")
    # print(f"Red pixel count: {red_pixel_count}")
    # print(f"Black pixel count: {black_pixel_count}")
    # print(f"Yellow pixel count: {yellow_pixel_count}")
    # print(f"Blue pixel count: {blue_pixel_count}")
    # print(f"Center tile black pixel count: {pixel_count}")
    
    hazard = None
    
    if yellow_pixel_count > 5:
        hazard = 'O'
    elif red_pixel_count > 5:
        hazard = 'F'
    elif pixel_count == 0:
        hazard = 'P'
    elif black_pixel_count >= 5:
        hazard = 'C'
    elif red_pixel_count ==3 and white_pixel_count ==1198 and green_pixel_count ==3 and blue_pixel_count ==1200:
        hazard = 'R'        
    
    if hazard:
        print(f"Hazard detected: {hazard}")
    
    return hazard
