# -*- coding: utf-8 -*-
import math


class CalSatePosi:
    __satNum = 0
    fileName = ""
    __satDict = {}
    __hour = 24
    __allData = []
    note = []
    __Day_of_Year = ""
    # ORBIT0
    af0 = [[0]*__hour for i in range(__satNum)]
    af1 = [[0]*__hour for i in range(__satNum)]
    af2 = [[0]*__hour for i in range(__satNum)]
    # ORBIT1
    aode = [[0]*__hour for i in range(__satNum)]
    crs = [[0]*__hour for i in range(__satNum)]
    deltan = [[0]*__hour for i in range(__satNum)]
    m0 = [[0]*__hour for i in range(__satNum)]
    # ORBIT2
    cuc = [[0]*__hour for i in range(__satNum)]
    e = [[0]*__hour for i in range(__satNum)]
    cus = [[0]*__hour for i in range(__satNum)]
    roota = [[0]*__hour for i in range(__satNum)]
    # ORBIT3
    toe = [[0]*__hour for i in range(__satNum)]
    cic = [[0]*__hour for i in range(__satNum)]
    omega0 = [[0]*__hour for i in range(__satNum)]
    cis = [[0]*__hour for i in range(__satNum)]
    # ORBIT4
    i0 = [[0]*__hour for i in range(__satNum)]
    crc = [[0]*__hour for i in range(__satNum)]
    omega = [[0]*__hour for i in range(__satNum)]
    omegadot = [[0]*__hour for i in range(__satNum)]
    # ORBIT5
    idot = [[0]*__hour for i in range(__satNum)]
    wn = [[0]*__hour for i in range(__satNum)]
    # ORBIT6
    precise = [[0]*__hour for i in range(__satNum)]
    health = [[0]*__hour for i in range(__satNum)]
    tgd = [[0]*__hour for i in range(__satNum)]
    idoc = [[0]*__hour for i in range(__satNum)]
    # ORBIT7
    starsec = [[0]*__hour for i in range(__satNum)]
    tlong = [[0]*__hour for i in range(__satNum)]
    X = [[0]*2880 for i in range(__satNum)]
    Y = [[0]*2880 for i in range(__satNum)]
    Z = [[0]*2880 for i in range(__satNum)]
    __GM = 3.986004E14
    __Ve = 7.2921151467E-14
    __pi = 3.1415926535897932
    __mu = 3.9860047000E14

    def __init__(self, fileName, satNum):
        self.__fileDir = fileName
        self.__satNum = satNum
        self.__Day_of_Year = fileName[-1][12:19]
        self.__readFile()
        self.__createDict()
        self.__sort()
        self.__calSatPosition()

    def __readFile(self):
        with open(self.fileName, "r", encoding="utf-8") as file:
            self.__allData = file.readlines()

    def __createDict(self):
        for i in range(61):
            if i < 10:
                self.__satDict["C "+str(i)] = i
                self.__satDict["C0"+str(i)] = i
            else:
                self.__satDict["C"+str(i)] = i

    def __sort(self):
        for i in range(len(self.__allData)):
            if self.__allData[i].strip() == "END OF HEADER":
                star = i + 1
                break
        for row in range(star, len(self.__allData), 8):
            year = int(self.__allData[row][4:8])
            month = int(self.__allData[row][9:11])
            day = int(self.__allData[row][12:14])
            if self.__Day_of_Year != self.__dayofYear(year, month, day):
                self.note.append("Exit yesterday's date!has abandoned.")
                continue
            hour = int(self.__allData[row][15:17])
            # 卫星编号从1开始，但数组从0开始
            satNum = self.__satDict[self.__allData[row][0:3]] - 1
            if self.__allData[row][0:3] in list(self.__satDict.keys()):
                self.__af0[satNum][hour] = \
                    self.__str2float(self.__allData[row][23:42])
                self.__af1[satNum][hour] = \
                    self.__str2float(self.__allData[row][42:61])
                self.__af2[satNum][hour] = \
                    self.__str2float(self.__allData[row][61:80])

                self.__aode[satNum][hour] = \
                    self.__str2float(self.__allData[row+1][4:23])
                self.__crs[satNum][hour] = \
                    self.__str2float(self.__allData[row+1][23:42])
                self.__deltan[satNum][hour] = \
                    self.__str2float(self.__allData[row+1][42:61])
                self.__m0[satNum][hour] = \
                    self.__str2float(self.__allData[row+1][61:80])

                self.__cuc[satNum][hour] = \
                    self.__str2float(self.__allData[row+2][4:23])
                self.__e[satNum][hour] = \
                    self.__str2float(self.__allData[row+2][23:42])
                self.__cus[satNum][hour] = \
                    self.__str2float(self.__allData[row+2][42:61])
                self.__roota[satNum][hour] = \
                    self.__str2float(self.__allData[row+2][61:80])

                self.__toe[satNum][hour] = \
                    self.__str2float(self.__allData[row+3][4:23])
                self.__cic[satNum][hour] = \
                    self.__str2float(self.__allData[row+3][23:42])
                self.__omega0[satNum][hour] = \
                    self.__str2float(self.__allData[row+3][42:61])
                self.__cis[satNum][hour] = \
                    self.__str2float(self.__allData[row+3][61:80])

                self.__i0[satNum][hour] = \
                    self.__str2float(self.__allData[row+4][4:23])
                self.__crc[satNum][hour] = \
                    self.__str2float(self.__allData[row+4][23:42])
                self.__omega[satNum][hour] = \
                    self.__str2float(self.__allData[row+4][42:61])
                self.__omegadot[satNum][hour] = \
                    self.__str2float(self.__allData[row+4][61:80])

                self.__idot[satNum][hour] = \
                    self.__str2float(self.__allData[row+5][4:23])
                self.__wn[satNum][hour] = \
                    self.__tr2float(self.__allData[row+5][42:61])

                self.__precise[satNum][hour] = \
                    self.__str2float(self.__allData[row+6][4:23])
                self.__health[satNum][hour] = \
                    self.__str2float(self.__allData[row+6][23:42])
                self.__tgd[satNum][hour] = \
                    self.__str2float(self.__allData[row+6][42:61])
                self.__idoc[satNum][hour] = \
                    self.__str2float(self.__allData[row+6][61:80])

                self.__starsec[satNum][hour] = \
                    self.__str2float(self.__allData[row+7][4:23])
                self.__tlong[satNum][hour] = \
                    self.__str2float(self.__allData[row+7][23:42])
            else:
                self.note.append("The Satellites number more than 60.\n \
                You need expend array!")

    def __calSatPosition(self):
        for oneNum in range(self.__satNum):
            for epoch in range(2880):
                T = 432000 + 30 * epoch
                time = 0
                for hour in range(24):
                    if abs(T-self.toe[oneNum][hour]) <= 1800:
                        time = hour
                sqrat = self.roota[oneNum][time]
                a = sqrat**2
                if a == 0.0:
                    continue
                n0 = pow(self.__GM/(a**3), 0.5)
                n = n0 + self.deltan[oneNum][time]
                tk = T - self.toe[oneNum][time] - 14.0
                if tk > 302400:
                    tk = tk - 604800
                elif tk < -302400:
                    tk = tk + 604800
                mk = self.m0[oneNum][time] + n * tk
                ek1 = mk
                ek2 = 1E10
                while abs(ek2-ek1) > 1E-20:
                    ek2 = mk + self.e[oneNum][time]*math.sin(ek1)
                    ek1 = ek2
                Ek = ek1
                sinfk = math.sqrt(1-(self.e[oneNum][time])**2)*math.sin(Ek) / \
                    (1 - (self.e[oneNum][time])*math.cos(Ek))
                cosfk = (math.cos(Ek) - self.e[oneNum][time]) / \
                    (1 - self.e[oneNum][time]*math.cos(Ek))
                fk = math.atan2(sinfk, cosfk)
                phik = fk + self.omega[oneNum][time]
                deltauk = self.cus[oneNum][time]*math.sin(2*phik) + \
                    self.cus[oneNum][time] * math.cos(2 * phik)
                deltark = self.crs[oneNum][time]*math.sin(2*phik) + \
                    self.crs[oneNum][time] * math.cos(2 * phik)
                deltaik = self.cis[oneNum][time]*math.sin(2*phik) + \
                    self.cis[oneNum][time] * math.cos(2 * phik)
                uk = phik + deltauk
                rk = a * (1 - self.e[oneNum][time])*math.cos(Ek) + deltark
                ik = self.i0[oneNum][time] + deltaik + \
                    self.idot[oneNum][time] * tk
                xk = rk * math.cos(uk)
                yk = rk * math.sin(uk)
                if oneNum <= 5:
                    Lk = self.omega0[oneNum][time] + \
                        self.omegadot[oneNum][time] * tk - \
                        self.__Ve * self.toe[oneNum][time]
                    tX1 = xk * math.cos(Lk) - yk * math.cos(ik) * math.sin(Lk)
                    tY1 = xk * math.cos(Lk) + yk * math.cos(ik) * math.cos(Lk)
                    tZ1 = yk * math.sin(ik)
                    delt_z = self.Ve * self.tk
                    delt_x = -5 * math.pi / 180
                    self.X[oneNum][epoch] = tX1 * math.cos(delt_z) + \
                        tY1 * math.cos(delt_x) * math.sin(delt_z) + \
                        tZ1 * math.sin(delt_x) * math.sin(delt_z)
                    self.Y[oneNum][epoch] = (-tX1) * math.sin(delt_z) + \
                        tY1 * math.cos(delt_x) * math.cos(delt_z) + \
                        tZ1 * math.sin(delt_x) * math.cos(delt_z)
                    self.Z[oneNum][epoch] = (-tY1) * math.sin(delt_x) + \
                        tZ1 * math.cos(delt_x)
                else:
                    Lk = self.omega0[oneNum][time] + \
                        (self.omegadot[oneNum][time] - self.Ve) * \
                        self.tk - self.Ve * self.toe[oneNum][time]
                    self.X[oneNum][epoch] = xk * math.cos(Lk) - \
                        yk * math.cos(ik) * math.sin(Lk)
                    self.Y[oneNum][epoch] = xk * math.sin(Lk) + \
                        yk * math.cos(ik) * math.cos(Lk)
                    self.Z[oneNum][epoch] = yk * math.sin(ik)

    def __dayofYear(self, year, month, day):
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

    def __str2float(str1):
        if str1.strip() == "":
            return 0.0
        else:
            return float(str1.replace("D", "E"))
