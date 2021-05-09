# -*- coding: utf-8 -*-
import math


def init():
    global satDict
    satDict = {}
    global fileDir
    fileDir = input("Please input file dir:")
    with open(fileDir, "r", encoding="utf-8") as file:
        global allData
        allData = file.readlines()
    global YEAR_MONTH_DAY
    YEAR_MONTH_DAY = fileDir.split("\\")[-1][12:19]
    createDict()
    global satNum
    satNum = 60
    hour = 24
    global af0
    global af1
    global af2
    global aode
    global crs
    global deltan
    global m0
    global cuc
    global e
    global cus
    global roota
    global toe
    global cic
    global omega0
    global cis
    global i0
    global crc
    global omega
    global omegadot
    global idot
    global wn
    global precise
    global health
    global tgd
    global idoc
    global starsec
    global tlong
    global X
    global Y
    global Z
    # ORBIT0
    af0 = [[0]*hour for i in range(satNum)]
    af1 = [[0]*hour for i in range(satNum)]
    af2 = [[0]*hour for i in range(satNum)]
    # ORBIT1
    aode = [[0]*hour for i in range(satNum)]
    crs = [[0]*hour for i in range(satNum)]
    deltan = [[0]*hour for i in range(satNum)]
    m0 = [[0]*hour for i in range(satNum)]
    # ORBIT2
    cuc = [[0]*hour for i in range(satNum)]
    e = [[0]*hour for i in range(satNum)]
    cus = [[0]*hour for i in range(satNum)]
    roota = [[0]*hour for i in range(satNum)]
    # ORBIT3
    toe = [[0]*hour for i in range(satNum)]
    cic = [[0]*hour for i in range(satNum)]
    omega0 = [[0]*hour for i in range(satNum)]
    cis = [[0]*hour for i in range(satNum)]
    # ORBIT4
    i0 = [[0]*hour for i in range(satNum)]
    crc = [[0]*hour for i in range(satNum)]
    omega = [[0]*hour for i in range(satNum)]
    omegadot = [[0]*hour for i in range(satNum)]
    # ORBIT5
    idot = [[0]*hour for i in range(satNum)]
    wn = [[0]*hour for i in range(satNum)]
    # ORBIT6
    precise = [[0]*hour for i in range(satNum)]
    health = [[0]*hour for i in range(satNum)]
    tgd = [[0]*hour for i in range(satNum)]
    idoc = [[0]*hour for i in range(satNum)]
    # ORBIT7
    starsec = [[0]*hour for i in range(satNum)]
    tlong = [[0]*hour for i in range(satNum)]
    X = [[0]*2880 for i in range(satNum)]
    Y = [[0]*2880 for i in range(satNum)]
    Z = [[0]*2880 for i in range(satNum)]
    global GM
    GM = 3.986004E14
    global Ve
    Ve = 7.2921151467E-14
    global pi
    pi = 3.1415926535897932
    global mu
    mu = 3.9860047000E14


def sort():
    for i in range(len(allData)):
        if allData[i].strip() == "END OF HEADER":
            star = i + 1
            break
    for row in range(star, len(allData), 8):
        year = int(allData[row][4:8])
        month = int(allData[row][9:11])
        day = int(allData[row][12:14])
        if YEAR_MONTH_DAY != dayofYear(year, month, day):
            print("Exit yesterday's date!\nhas abandoned")
            continue
        hour = int(allData[row][15:17])
        # 卫星编号从1开始，但数组从0开始
        satNum = satDict[allData[row][0:3]] - 1
        if allData[row][0:3] in list(satDict.keys()):
            af0[satNum][hour] = str2float(allData[row][23:42])
            af1[satNum][hour] = str2float(allData[row][42:61])
            af2[satNum][hour] = str2float(allData[row][61:80])

            aode[satNum][hour] = str2float(allData[row+1][4:23])
            crs[satNum][hour] = str2float(allData[row+1][23:42])
            deltan[satNum][hour] = str2float(allData[row+1][42:61])
            m0[satNum][hour] = str2float(allData[row+1][61:80])

            cuc[satNum][hour] = str2float(allData[row+2][4:23])
            e[satNum][hour] = str2float(allData[row+2][23:42])
            cus[satNum][hour] = str2float(allData[row+2][42:61])
            roota[satNum][hour] = str2float(allData[row+2][61:80])

            toe[satNum][hour] = str2float(allData[row+3][4:23])
            cic[satNum][hour] = str2float(allData[row+3][23:42])
            omega0[satNum][hour] = str2float(allData[row+3][42:61])
            cis[satNum][hour] = str2float(allData[row+3][61:80])

            i0[satNum][hour] = str2float(allData[row+4][4:23])
            crc[satNum][hour] = str2float(allData[row+4][23:42])
            omega[satNum][hour] = str2float(allData[row+4][42:61])
            omegadot[satNum][hour] = str2float(allData[row+4][61:80])

            idot[satNum][hour] = str2float(allData[row+5][4:23])
            wn[satNum][hour] = str2float(allData[row+5][42:61])

            precise[satNum][hour] = str2float(allData[row+6][4:23])
            health[satNum][hour] = str2float(allData[row+6][23:42])
            tgd[satNum][hour] = str2float(allData[row+6][42:61])
            idoc[satNum][hour] = str2float(allData[row+6][61:80])

            starsec[satNum][hour] = str2float(allData[row+7][4:23])
            tlong[satNum][hour] = str2float(allData[row+7][23:42])
        else:
            print("The Satellites number more than 60.\n \
            You need expend array!")


def satPosition():
    for oneNum in range(satNum):
        for epoch in range(2880):
            T = 432000 + 30 * epoch
            time = 0
            for hour in range(24):
                if abs(T-toe[oneNum][hour]) <= 1800:
                    time = hour
            sqrat = roota[oneNum][time]
            a = sqrat**2
            if a == 0.0:
                continue
            n0 = pow(GM/(a**3), 0.5)
            n = n0 + deltan[oneNum][time]
            tk = T - toe[oneNum][time] - 14.0
            if tk > 302400:
                tk = tk - 604800
            elif tk < -302400:
                tk = tk + 604800
            mk = m0[oneNum][time] + n * tk
            ek1 = mk
            ek2 = 1E10
            while abs(ek2-ek1) > 1E-20:
                ek2 = mk + e[oneNum][time]*math.sin(ek1)
                ek1 = ek2
            Ek = ek1
            sinfk = math.sqrt(1-(e[oneNum][time])**2)*math.sin(Ek) / \
                (1 - (e[oneNum][time])*math.cos(Ek))
            cosfk = (math.cos(Ek) - e[oneNum][time]) / \
                (1 - e[oneNum][time]*math.cos(Ek))
            fk = math.atan2(sinfk, cosfk)
            phik = fk + omega[oneNum][time]
            deltauk = cus[oneNum][time]*math.sin(2*phik) + \
                cus[oneNum][time] * math.cos(2 * phik)
            deltark = crs[oneNum][time]*math.sin(2*phik) + \
                crs[oneNum][time] * math.cos(2 * phik)
            deltaik = cis[oneNum][time]*math.sin(2*phik) + \
                cis[oneNum][time] * math.cos(2 * phik)
            uk = phik + deltauk
            rk = a * (1-e[oneNum][time])*math.cos(Ek) + deltark
            ik = i0[oneNum][time] + deltaik + idot[oneNum][time] * tk
            xk = rk * math.cos(uk)
            yk = rk * math.sin(uk)
            if oneNum <= 5:
                Lk = omega0[oneNum][time] + omegadot[oneNum][time] * tk - \
                    Ve * toe[oneNum][time]
                tX1 = xk * math.cos(Lk) - yk * math.cos(ik) * math.sin(Lk)
                tY1 = xk * math.cos(Lk) + yk * math.cos(ik) * math.cos(Lk)
                tZ1 = yk * math.sin(ik)
                delt_z = Ve * tk
                delt_x = -5 * math.pi / 180
                X[oneNum][epoch] = tX1 * math.cos(delt_z) + \
                    tY1 * math.cos(delt_x) * math.sin(delt_z) + \
                    tZ1 * math.sin(delt_x) * math.sin(delt_z)
                Y[oneNum][epoch] = (-tX1) * math.sin(delt_z) + \
                    tY1 * math.cos(delt_x) * math.cos(delt_z) + \
                    tZ1 * math.sin(delt_x) * math.cos(delt_z)
                Z[oneNum][epoch] = (-tY1) * math.sin(delt_x) + \
                    tZ1 * math.cos(delt_x)
            else:
                Lk = omega0[oneNum][time] + (omegadot[oneNum][time] - Ve) * \
                    tk - Ve * toe[oneNum][time]
                X[oneNum][epoch] = xk * math.cos(Lk) - \
                    yk * math.cos(ik) * math.sin(Lk)
                Y[oneNum][epoch] = xk * math.sin(Lk) + \
                    yk * math.cos(ik) * math.cos(Lk)
                Z[oneNum][epoch] = yk * math.sin(ik)


def outStream():
    fileName = fileDir.split("\\")[-1][0:-4] + "SatellitePosition.txt"
    fileOut = open(fileName, "w", encoding="utf-8")
    fileOut.write("{:<9}".format("Epoch"))
    fileOut.write("{:<15}".format("X"))
    fileOut.write("{:<15}".format("Y"))
    fileOut.write("{:<15}".format("Z"))
    fileOut.write("\n")
    for i in range(satNum):
        fileOut.write("C" + "{:0>2d}".format(i+1)+"Satellite")
        fileOut.write("\n")
        for j in range(2880):
            fileOut.write(hourMinuteSecond(j*30))
            fileOut.write("{:<15.3f}".format(X[i][j]))
            fileOut.write("{:<15.3f}".format(Y[i][j]))
            fileOut.write("{:<15.3f}".format(Z[i][j]))
            fileOut.write("\n")
    fileOut.close()


def str2float(str1):
    if str1.strip() == "":
        return 0.0
    else:
        return float(str1.replace("D", "E"))


def createDict():
    for i in range(61):
        if i < 10:
            satDict["C "+str(i)] = i
            satDict["C0"+str(i)] = i
        else:
            satDict["C"+str(i)] = i


def dayofYear(year, month, day):
    months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    days = months[month-1] + day
    if ((year % 400 == 0) or (year % 100 != 0 and year % 4 == 0))\
            and (month > 2):
        days = days + 1
    strDate = str(year)
    if days < 10:
        strDate = strDate + "00" + str(days)
    elif days < 100:
        strDate = strDate + "0" + str(days)
    else:
        strDate = strDate + str(days)
    return strDate


def hourMinuteSecond(epoch):
    hour = int(epoch/3600)
    deltaMinute = (epoch/3600 - hour) * 60
    if abs(round(deltaMinute) - deltaMinute) < 1E-13:
        minute = round((epoch/3600 - hour) * 60)
        second = 0
    else:
        minute = int((epoch/3600 - hour) * 60)
        second = round(((epoch/3600 - hour) * 60 - minute) * 60)
        # deltaSecond = (epoch/3600 - hour) * 60
        # if abs(round(deltaSecond) - deltaSecond) < 1E-16:
        #     minute = round((epoch/3600 - hour) * 60)
        #     second = 0
        # else:
        #     minute = int((epoch/3600 - hour) * 60)
        #     second = round(((epoch/3600 - hour) * 60 - minute) * 60)
    return "{0:0>2d}:{1:0>2d}:{2:0>2d} ".format(hour, minute, second)


if __name__ == "__main__":
    init()
    sort()
    satPosition()
    outStream()
    print("end!")
