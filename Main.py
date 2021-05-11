# -*- coding: utf-8 -*-
import os
from ClassCalSatePosi import CalSatePosi


def init():
    global satNum
    satNum = 60
    if os.path.exists("./data"):
        for fileName in os.listdir("./data"):
            global satPosition
            satPosition = CalSatePosi(fileName, satNum)
            outStream()
            del satPosition
    else:
        print("数据不存在！")


def outStream():
    fileName = satPosition.fileName[0:-4] + "SatellitePosition.txt"
    if os.path.exists("./output/" + satPosition.fileName):
        return
    else:
        fileOut = open("./output/" + fileName, "w", encoding="utf-8")
        fileOut.write("{:<9}".format("Epoch"))
        fileOut.write("{:<15}".format("X"))
        fileOut.write("{:<15}".format("Y"))
        fileOut.write("{:<15}".format("Z"))
        fileOut.write("\n")
        for i in range(satNum):
            fileOut.write("C" + "{:0>2d}".format(i+1)+"Satellite")
            fileOut.write("\n")
            for j in range(2880):
                fileOut.write(timeFormat(j*30))
                fileOut.write("{:<15.3f}".format(satPosition.X[i][j]))
                fileOut.write("{:<15.3f}".format(satPosition.Y[i][j]))
                fileOut.write("{:<15.3f}".format(satPosition.Z[i][j]))
                fileOut.write("\n")
        fileOut.close()


def timeFormat(epoch):
    hour = int(epoch/3600)
    deltaMinute = (epoch/3600 - hour) * 60
    if abs(round(deltaMinute) - deltaMinute) < 1E-13:
        minute = round((epoch/3600 - hour) * 60)
        second = 0
    else:
        minute = int((epoch/3600 - hour) * 60)
        second = round(((epoch/3600 - hour) * 60 - minute) * 60)
    return "{0:0>2d}:{1:0>2d}:{2:0>2d} ".format(hour, minute, second)


if __name__ == "__main__":
    init()
    print("end!")
