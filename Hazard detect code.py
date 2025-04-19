







def hazarddet(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    upper_yellow = np.array([20 , 100 , 100 ])
    lower_yellow = np.array([30 , 255 , 255 ])

    upper_yellow2 = np.array([20 , 100 , 100 ])
    lower_yellow2 = np.array([30 , 255 , 255 ])

    yellowmask1=cv2.inRange(hsv,upper_yellow , lower_yellow)

    yellowmask2=cv2.inRange(hsv, upper_yellow2 , lower_yellow2)

    mainyellow= yellowmask1 + yellowmask2


    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    lower_black1 = np.array([0, 0, 0])
    upper_black1 = np.array([180, 255, 100])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_pixel_count = cv2.countNonZero(red_mask)

    black_mask = cv2.inRange(hsv, lower_black1, upper_black1)
    black_pixel_count = cv2.countNonZero(black_mask)
    yellow_pixel_count= cv2.countNonZero(mainyellow)

    wheel_left.setVelocity(0.0)
    wheel_right.setVelocity(0.0)

    height, width, _ = hsv.shape
    tile_h = height // 3
    tile_w = width // 3

    tiles = []
    cv2.imwrite(f"c:/Users/CYBER-TECH/Desktop/saves/Tile {i+1}.png", tile)
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

    print(f"Number of red pixels: {red_pixel_count}")

    victimType = None

    print("black pixel count :", pixel_count)

    print("yellow pixel coun is : ",yellow_pixel_count)

    
    
    
    
    
    
    if yellow_pixel_count > 5:
        print("ORGANIC PEROXIDE")
        victimType = bytes('O', "utf-8")


    elif red_pixel_count > 5:
        print("FLAMMABLE GAS")
        victimType = bytes('F', "utf-8")




    elif pixel_count == 0:
        print("POISON")
        victimType = bytes('P', "utf-8")

    elif black_pixel_count >= 5:
        print("CORROSIVE")
        victimType = bytes('C', "utf-8")

    if victimType:
        position = gps.getValues()
        x = int(position[0] * 100)  
        y = int(position[2] * 100)

        
        if not is_victim_already_saved(x, y, victim_positions):
            victim_positions.append((x, y))  

            message = struct.pack("i i c", x, y, victimType)
            robot.step(1500)
            emitter.send(message)
            robot.step(1500)
            sign[0] = True
        else:
            print(f"Victim at ({x}, {y}) already saved. Skipping...")
