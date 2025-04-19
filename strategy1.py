def strategy_1():
    if (robot.step(timestep)==-1):
        return
    
    rotate_right()

    sign=Scan_Camera1() #return el red ymin wla shmal
    if sign=='l':
        for i in range(0,4):
            move_tile_forward()
        
    else:
        for i in range(0,3):
            move_tile_backward()
    strategy_2()
    return
