def respawn():

    if receiver.getQueueLength() > 0:  # If receiver queue is not empty
        receivedData = receiver.getBytes()
        tup = struct.unpack('c', receivedData)  # Parse data into character
        if tup[0].decode("utf-8") == 'L':  # 'L' means lack of progress occurred
            print("Detected Lack of Progress!")
            receiver.nextPacket()
            return True
        receiver.nextPacket()  # Discard the current data packet
