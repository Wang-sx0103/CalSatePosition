# -*- coding: utf-8 -*-
import math


class CalSatePosi(object):
    def __init__(self, fileName, satNum):
        self.fileName = fileName
        self.__satNum = satNum
        __hour = 24
        __satNum = satNum
        self.__allData = []
        self.note = []
        self.__satDict = {}
        # ORBIT0
        self.__af0 = [[0]*__hour for i in range(__satNum)]
        self.__af1 = [[0]*__hour for i in range(__satNum)]
        self.__af2 = [[0]*__hour for i in range(__satNum)]
        # ORBIT1
        self.__aode = [[0]*__hour for i in range(__satNum)]
        self.__crs = [[0]*__hour for i in range(__satNum)]
        self.__deltan = [[0]*__hour for i in range(__satNum)]
        self.__m0 = [[0]*__hour for i in range(__satNum)]
        # ORBIT2
        self.__cuc = [[0]*__hour for i in range(__satNum)]
        self.__e = [[0]*__hour for i in range(__satNum)]
        self.__cus = [[0]*__hour for i in range(__satNum)]
        self.__roota = [[0]*__hour for i in range(__satNum)]
        # ORBIT3
        self.__toe = [[0]*__hour for i in range(__satNum)]
        self.__cic = [[0]*__hour for i in range(__satNum)]
        self.__omega0 = [[0]*__hour for i in range(__satNum)]
        self.__cis = [[0]*__hour for i in range(__satNum)]
        # ORBIT4
        self.__i0 = [[0]*__hour for i in range(__satNum)]
        self.__crc = [[0]*__hour for i in range(__satNum)]
        self.__omega = [[0]*__hour for i in range(__satNum)]
        self.__omegadot = [[0]*__hour for i in range(__satNum)]
        # ORBIT5
        self.__idot = [[0]*__hour for i in range(__satNum)]
        self.__wn = [[0]*__hour for i in range(__satNum)]
        # ORBIT6
        self.__precise = [[0]*__hour for i in range(__satNum)]
        self.__health = [[0]*__hour for i in range(__satNum)]
        self.__tgd = [[0]*__hour for i in range(__satNum)]
        self.__idoc = [[0]*__hour for i in range(__satNum)]
        # ORBIT7
        self.__starsec = [[0]*__hour for i in range(__satNum)]
        self.__tlong = [[0]*__hour for i in range(__satNum)]
        self.X = [[0]*2880 for i in range(__satNum)]
        self.Y = [[0]*2880 for i in range(__satNum)]
        self.Z = [[0]*2880 for i in range(__satNum)]
        self.__GM = 3.986004E14
        self.__Ve = 7.2921151467E-14
        self.__pi = 3.1415926535897932
        self.__mu = 3.9860047000E14
        self.__Day_of_Year = fileName[12:19]
        self.__readFile()
        self.__createDict()
        self.__sort()
        self.__calSatPosition()

    def __readFile(self):
        with open("./data/"+self.fileName, "r", encoding="utf-8") as file:
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
                    self.__str2float(self.__allData[row+5][42:61])

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
                    if abs(T-self.__toe[oneNum][hour]) <= 1800:
                        time = hour
                sqrat = self.__roota[oneNum][time]
                a = sqrat**2
                if a == 0.0:
                    continue
                n0 = pow(self.__GM/(a**3), 0.5)
                n = n0 + self.__deltan[oneNum][time]
                tk = T - self.__toe[oneNum][time] - 14.0
                if tk > 302400:
                    tk = tk - 604800
                elif tk < -302400:
                    tk = tk + 604800
                mk = self.__m0[oneNum][time] + n * tk
                ek1 = mk
                ek2 = 1E10
                while abs(ek2-ek1) > 1E-20:
                    ek2 = mk + self.__e[oneNum][time]*math.sin(ek1)
                    ek1 = ek2
                Ek = ek1
                sinfk = math.sqrt(1-(self.__e[oneNum][time])**2) * \
                    math.sin(Ek)/(1 - (self.__e[oneNum][time])*math.cos(Ek))
                cosfk = (math.cos(Ek) - self.__e[oneNum][time]) / \
                    (1 - self.__e[oneNum][time]*math.cos(Ek))
                fk = math.atan2(sinfk, cosfk)
                phik = fk + self.__omega[oneNum][time]
                deltauk = self.__cus[oneNum][time]*math.sin(2*phik) + \
                    self.__cus[oneNum][time] * math.cos(2 * phik)
                deltark = self.__crs[oneNum][time]*math.sin(2*phik) + \
                    self.__crs[oneNum][time] * math.cos(2 * phik)
                deltaik = self.__cis[oneNum][time]*math.sin(2*phik) + \
                    self.__cis[oneNum][time] * math.cos(2 * phik)
                uk = phik + deltauk
                rk = a * (1 - self.__e[oneNum][time])*math.cos(Ek) + deltark
                ik = self.__i0[oneNum][time] + deltaik + \
                    self.__idot[oneNum][time] * tk
                xk = rk * math.cos(uk)
                yk = rk * math.sin(uk)
                if oneNum <= 5:
                    Lk = self.__omega0[oneNum][time] + \
                        self.__omegadot[oneNum][time] * tk - \
                        self.__Ve * self.__toe[oneNum][time]
                    tX1 = xk * math.cos(Lk) - yk * math.cos(ik) * math.sin(Lk)
                    tY1 = xk * math.cos(Lk) + yk * math.cos(ik) * math.cos(Lk)
                    tZ1 = yk * math.sin(ik)
                    delt_z = self.__Ve * tk
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
                    Lk = self.__omega0[oneNum][time] + \
                        (self.__omegadot[oneNum][time] - self.__Ve) * \
                        tk - self.__Ve * self.__toe[oneNum][time]
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

    def __str2float(self, str1):
        if str1.strip() == "":
            return 0.0
        else:
            return float(str1.replace("D", "E"))
