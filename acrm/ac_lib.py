import ac
import acsys
import sys
import os
from math import sin, cos
import platform

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/../stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/../stdlib'

sys.path.insert(0, sysdir)
sys.path.insert(0, os.path.dirname(__file__) + '/../third_party')
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info


def formatTime(millis):
    millis = int(millis)
    m = int(millis / 60000)
    s = int((millis % 60000) / 1000)
    ms = millis % 1000

    return "{:02d}:{:02d}.{:03d}".format(m, s, ms)


def formatGear(gear):
    if gear == 0:
        return "R"
    elif gear == 1:
        return "N"
    else:
        return str(gear - 1)


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GL:
    @staticmethod
    def line(x1, y1, x2, y2, color=Color(1, 1, 1, 1)):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        ac.glBegin(1)
        ac.glVertex2f(x1, y1)
        ac.glVertex2f(x2, y2)
        ac.glEnd()

    @staticmethod
    def rect(x, y, w, h, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glQuad(x, y, w, h)
        else:
            ac.glBegin(1)
            ac.glVertex2f(x, y)
            ac.glVertex2f(x + w, y)
            ac.glVertex2f(x + w, y)
            ac.glVertex2f(x + w, y + h)
            ac.glVertex2f(x + w, y + h)
            ac.glVertex2f(x, y + h)
            ac.glVertex2f(x, y + h)
            ac.glVertex2f(x, y)
            ac.glEnd()

    @staticmethod
    def circle(x, y, radius, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        start = 0
        stop = 360
        sample = 36 * radius
        while start <= stop:
            rad1 = start
            rad2 = min(start + 1, stop)
            ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            if filled:
                ac.glVertex2f(x, y)

            start += sample

        ac.glEnd()

    @staticmethod
    def arc(x, y, radius, start=0, stop=360, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        sample = (stop - start) / (36 * radius)
        while start <= stop:
            rad1 = start
            rad2 = min(start + 1, stop)
            ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            if filled:
                ac.glVertex2f(x, y)

            start += sample

        ac.glEnd()

    @staticmethod
    def donut(x, y, radius, width, start=0, stop=360, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        sample = (stop - start) / (36 * radius)
        while start <= stop:
            rad1 = start
            rad2 = min(start + 1, stop)
            ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            ac.glVertex2f(x + cos(rad1) * (radius - width), y - sin(rad1) * (radius - width))
            ac.glVertex2f(x + cos(rad2) * (radius - width), y - sin(rad2) * (radius - width))
            if filled:
                ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
                ac.glVertex2f(x + cos(rad1) * (radius - width), y - sin(rad1) * (radius - width))

            start += sample

        ac.glEnd()

    @staticmethod
    def polygon(points, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        for i in points:
            if isinstance(i, Point):
                ac.glVertex2f(i.x, i.y)

        ac.glEnd()


class ACPLAYER:
    @staticmethod
    def getPlayerNickname():
        return info.static.playerNick

    @staticmethod
    def getPlayerFirstname():
        return info.static.playerName

    @staticmethod
    def getPlayerLastname():
        return info.static.playerSurname


class ACSESSION:
    @staticmethod
    def getSessionType():
        return info.graphics.session

    @staticmethod
    def getSessionStatus():
        return info.graphics.status

    @staticmethod
    def isTimedRace():
        return info.static.isTimedRace

    @staticmethod
    def getRaceTimeLeft():
        return info.graphics.sessionTimeLeft

    @staticmethod
    def getTrackLength():
        return ac.getTrackLength(0)

    @staticmethod
    def getTrackName():
        return ac.getTrackName(0)

    @staticmethod
    def getCarsCount():
        return ac.getCarsCount()


class ACLAP:
    @staticmethod
    def getCurrentLapTime(car=0):
        return ac.getCarState(car, acsys.CS.LapTime)

    @staticmethod
    def getCurrentLap(car=0):
        time = ac.getCarState(car, acsys.CS.LapTime)
        if time > 0:
            return formatTime(time)
        else:
            return "00:00.000"

    @staticmethod
    def getLastLapTime(car=0):
        return ac.getCarState(car, acsys.CS.LastLap)

    @staticmethod
    def getLastLap(car=0):
        time = ac.getCarState(car, acsys.CS.LastLap)
        if time > 0:
            return formatTime(time)
        else:
            return "00:00.000"

    @staticmethod
    def getBestLapTime(car=0):
        return ac.getCarState(car, acsys.CS.BestLap)

    @staticmethod
    def getBestLap(car=0):
        time = ac.getCarState(car, acsys.CS.BestLap)
        if time > 0:
            return formatTime(time)
        else:
            return "00:00.000"

    @staticmethod
    def getSplit():
        return info.graphics.split

    @staticmethod
    def getSplits(car=0):
        return ac.getLastSplits(car)

    @staticmethod
    def getLap(car=0):
        return ac.getCarState(car, acsys.CS.LapCount) + 1

    @staticmethod
    def getLapDeltaTime(car=0):
        return ac.getCarState(car, acsys.CS.PerformanceMeter)

    @staticmethod
    def getLapDelta(car=0):
        time = ac.getCarState(car, acsys.CS.PerformanceMeter) * 1000
        if time != 0:
            if time < 0:
                return "-" + formatTime(abs(time))
            elif time > 0:
                return "+" + formatTime(abs(time))
        else:
            return "-00:00.000"

    @staticmethod
    def isLapInvalidated(car=0):
        return ac.getCarState(car, acsys.CS.LapInvalidated) or ACCAR.getTyresOut() > 2 or ACCAR.isInPit()

    @staticmethod
    def getLaps():
        if info.graphics.numberOfLaps > 0:
            return info.graphics.numberOfLaps
        else:
            return "-"

    @staticmethod
    def lastSectorTime():
        return info.graphics.lastSectorTime

    @staticmethod
    def getSectors():
        return info.static.sectorCount


class ACCAR:
    @staticmethod
    def getFocusedCar():
        return ac.getFocusedCar()

    @staticmethod
    def getCarDamage(loc=0):
        # 0: Front, 1: Rear, 2: Left, 3: Right, 4:
        return info.physics.carDamage[loc]

    @staticmethod
    def getPrevCarDiffTime():
        time = 0
        track_len = ACSESSION.getTrackLength()
        lap = ACLAP.getLap(0)
        pos = ACCAR.getLocation(0)

        for car in range(ACSESSION.getCarsCount()):
            if ACCAR.getPosition(car) == ACCAR.getPosition(0) - 1:
                lap_next = ACLAP.getLap(car)
                pos_next = ACCAR.getLocation(car)

                dist = max(0, (pos_next * track_len + lap_next * track_len) - (pos * track_len + lap * track_len))
                time = max(0.0, dist / max(10.0, ACCAR.getSpeed(0, "ms")))
                break
        return time

    @staticmethod
    def getPrevCarDiff():
        time = ACCAR.getPrevCarDiffTime()
        dist = 0
        track_len = ACSESSION.getTrackLength()
        if dist > track_len:
            laps = dist / track_len
            if laps > 1:
                return " +{:3.1f}".format(laps) + " Laps"
            else:
                return " +{:3.1f}".format(laps) + " Lap"
        else:
            return "+" + formatTime(int(time * 1000))

    @staticmethod
    def getNextCarDiffTime():
        time = 0
        dist = 0
        track_len = ACSESSION.getTrackLength()
        lap = ACLAP.getLap(0)
        pos = ACCAR.getLocation(0)

        for car in range(ACSESSION.getCarsCount()):
            if ACCAR.getPosition(car) == ACCAR.getPosition(0) + 1:
                lap_next = ACLAP.getLap(car)
                pos_next = ACCAR.getLocation(car)

                dist = max(0, (pos * track_len + lap * track_len) - (pos_next * track_len + lap_next * track_len))
                time = max(0.0, dist / max(10.0, ACCAR.getSpeed(car, "ms")))
                break
        return time

    @staticmethod
    def getNextCarDiff():
        time = ACCAR.getNextCarDiffTime()
        dist = 0
        track_len = ACSESSION.getTrackLength()

        if dist > track_len:
            laps = dist / track_len
            if laps > 1:
                return " -{:3.1f}".format(laps) + " Laps"
            else:
                return " -{:3.1f}".format(laps) + " Lap"
        else:
            return "-" + formatTime(int(time * 1000))

    @staticmethod
    def getGas():
        return info.physics.gas

    @staticmethod
    def getBrake():
        return info.physics.brake

    @staticmethod
    def hasDRS():
        return info.static.hasDRS

    @staticmethod
    def DRSEnabled():
        return info.physics.drsEnabled

    @staticmethod
    def hasERS():
        return info.static.hasERS

    @staticmethod
    def hasKERS():
        return info.static.hasKERS

    @staticmethod
    def ABS():
        return info.physics.abs

    @staticmethod
    def getSpeed(car=0, unit="kmh"):
        if unit == "kmh":
            return ac.getCarState(car, acsys.CS.SpeedKMH)
        elif unit == "mph":
            return ac.getCarState(car, acsys.CS.SpeedMPH)
        elif unit == "ms":
            return ac.getCarState(car, acsys.CS.SpeedMS)

    @staticmethod
    def getGear(car=0):
        return formatGear(ac.getCarState(car, acsys.CS.Gear))

    @staticmethod
    def getRPM(car=0):
        return ac.getCarState(car, acsys.CS.RPM)

    @staticmethod
    def getRPMMax():
        if info.static.maxRpm:
            return info.static.maxRpm
        else:
            return 8000

    @staticmethod
    def getPosition(car=0):
        return ac.getCarRealTimeLeaderboardPosition(car) + 1

    @staticmethod
    def getLocation(car=0):
        return ac.getCarState(car, acsys.CS.NormalizedSplinePosition)

    @staticmethod
    def isInPit(car=0):
        return ac.isCarInPitline(car) or ac.isCarInPit(car)

    @staticmethod
    def isAIDriven():
        return info.physics.isAIControlled

    @staticmethod
    def getFuel():
        return info.physics.fuel

    @staticmethod
    def getMaxFuel():
        return info.static.maxFuel

    @staticmethod
    def getTyresOut():
        return info.physics.numberOfTyresOut

    @staticmethod
    def getTyreWearValue(tyre=0):
        return info.physics.tyreWear[tyre]

    @staticmethod
    def getTyreWear(tyre=0):
        return (ACCAR.getTyreWearValue(tyre) - 94) * 16.6

    @staticmethod
    def getTyreDirtyLevel(tyre=0):
        return info.physics.tyreDirtyLevel[tyre]

    @staticmethod
    def getTyreCompund():
        return info.graphics.tyreCompound

    @staticmethod
    def getCarModel():
        return info.static.carModel

    @staticmethod
    def getTyreTemp(tyre=0, loc="m"):
        if loc == "i":
            return info.physics.tyreTempI[tyre]
        elif loc == "m":
            return info.physics.tyreTempM[tyre]
        elif loc == "o":
            return info.physics.tyreTempO[tyre]
        elif loc == "c":
            return info.physics.tyreCoreTemperature[tyre]

    @staticmethod
    def getTyrePressure(tyre=0):
        return info.physics.wheelsPressure[tyre]

    @staticmethod
    def getBrakeTemperature(tyre=0):
        return info.physics.brakeTemp[tyre]
