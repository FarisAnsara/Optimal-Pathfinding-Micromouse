import API
import sys
import LeftWall
import Flood

# def log(string):
#     sys.stderr.write("{}\n".format(string))
#     sys.stderr.flush()
# 
# def main():
#     log("Running...")
#     API.setColor(0, 0, "G")
#     API.setText(0, 0, "abc")
#     while True:
#         if not API.wallLeft():
#             API.turnLeft()
#         while API.wallFront():
#             API.turnRight()
#         # API.setColor(0, 0, "b")
#         API.moveForward()



if __name__ == "__main__":
    Flood.main()


