import sys
import API

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def follower():
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "abc")
    while True:
        if not API.wallLeft():
            API.turnLeft()
        while API.wallFront():
            API.turnRight()
        API.moveForward()