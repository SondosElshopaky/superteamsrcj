def startegy_2():
    if (robot.step(timestep)==-1):
        return

    sign = Scan_Camera2() #return el red ymin wla shmal
    if sign=='r':
        for i in range(0,4):
            move_tile_forward()
        
    else:
        for i in range(0,3):
            move_tile_backward()

        rotate_left()
        move_tile_forward()
        rotate_right()

        for i in range(0,3):
            move_tile_forward()

        rotate_left()
        move_tile_forward()

        sign = Scan_Camera2()

        move_tile_forward()
        if sign == 'r':
            rotate_right()
            for i in range(0,4):
                move_tile_forward()
        else:
            rotate_left()
            for i in range(0,3):
                move_tile_forward()

    strategy_3()
    return
