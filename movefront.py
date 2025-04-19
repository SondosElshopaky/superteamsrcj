def movefront():  # need delay in beginning to work min 2 scs
    angles = imu.getRollPitchYaw()  # Step 4: Use the getValue() function to get the sensor reading
    angles = convert(math.degrees(angles[2]))
    ###################################### NORTH ##############################################
    if 1 > angles or angles > 359:
        zcurrent = round(gps.getValues()[2], 3)
        zfinish = zcurrent - 0.12
        # print("1.current", zcurrent, " end:", zfinish)
        while robot.step(timestep) != -1:
            zcurrent = imu.getRollPitchYaw()
            zcurrent = round(gps.getValues()[2], 3)
            # print("2.current", zcurrent, " end:", zfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (zfinish - 0.001) <= zcurrent <= (zfinish + 0.001):
                # print("3.current", zcurrent, " end:", zfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break


    ########################################## EAST ###############################################
    elif 89 <= angles <= 91:
        # print("entered if condtion")
        xcurrent = round(gps.getValues()[0], 3)
        xfinish = xcurrent + 0.12
        # print("1.current", xcurrent, " end:", xfinish)
        while robot.step(timestep) != -1:
            xcurrent = imu.getRollPitchYaw()
            xcurrent = round(gps.getValues()[0], 3)
            # print("2.current", xcurrent, " end:", xfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (xfinish - 0.001) <= xcurrent <= (xfinish + 0.001):
                # print("3.current", xcurrent, " end:", xfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break


    ########################################## WEST ###############################################
    elif 269 <= angles <= 271:
        # print("entered if condtion")
        xcurrent = round(gps.getValues()[0], 3)
        xfinish = xcurrent - 0.12
        # print("1.current", xcurrent, " end:", xfinish)
        while robot.step(timestep) != -1:
            xcurrent = imu.getRollPitchYaw()
            xcurrent = round(gps.getValues()[0], 3)
            # print("2.current", xcurrent, " end:", xfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (xfinish - 0.001) <= xcurrent <= (xfinish + 0.001):
                # print("3.current", xcurrent, " end:", xfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break
    ############################################# SOUTH #############################################
    elif 179 <= angles <= 181:
        # print("entered if condtion")
        zcurrent = round(gps.getValues()[2], 3)
        zfinish = zcurrent + 0.12
        # print("1.current", zcurrent, " end:", zfinish)
        while robot.step(timestep) != -1:
            zcurrent = round(gps.getValues()[2], 3)
            # print("2.current", zcurrent, " end:", zfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (zfinish - 0.001) <= zcurrent <= (zfinish + 0.001):
                # print("3.current", zcurrent, " end:", zfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break
    else:
        correction()
        print("not in any directions >3")
