from python_helper import Constant as c
from python_helper import ObjectHelper, DateTimeHelper, log

from constant import IntervalConstant


def getCurrentClosingDateTime(givenDateTime, closingDay, dueDay, reference):
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    if isLastMonthDay(closingDay):
        return getCurrentClosingDateTime(givenDateTime, getLastMonthDayFromDateTimeAsStringList(givenDateTimeAsStringList), dueDay, reference)
    if isLastMonthDay(dueDay):
        return getCurrentClosingDateTime(givenDateTime, closingDay, getLastMonthDayFromDateTimeAsStringList(givenDateTimeAsStringList), reference)
    if ObjectHelper.equals(IntervalConstant.CLOSING_DAY_REFERENCE, reference):
        currentClosingDateTime = buildFromDateTimeAsStringList(givenDateTimeAsStringList, closingDay)
        return currentClosingDateTime if givenDateTime <= currentClosingDateTime else nextMonth(currentClosingDateTime)
    if ObjectHelper.equals(IntervalConstant.DUE_DAY_REFERENCE, reference):
        currentClosingDateTime = buildFromDateTimeAsStringList(givenDateTimeAsStringList, closingDay)
        currentDueDateTime = buildFromDateTimeAsStringList(givenDateTimeAsStringList, dueDay)
        if givenDateTime <= currentDueDateTime:
            return currentClosingDateTime if currentClosingDateTime < currentDueDateTime else previousMonth(currentClosingDateTime)
        else:
            nextCurrentClosingDateTime = nextMonth(currentClosingDateTime)
            nextCurrentDueDateTime = nextMonth(currentDueDateTime)
            return nextCurrentClosingDateTime if nextCurrentClosingDateTime < nextCurrentDueDateTime else previousMonth(nextCurrentClosingDateTime)


def getNextClosingDateTime(givenDateTime, closingDay, dueDay, reference):
    return nextMonth(getCurrentClosingDateTime(givenDateTime, closingDay, dueDay, reference))


def getCurrentDueDateTime(givenDateTime, closingDay, dueDay, reference):
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    if isLastMonthDay(closingDay):
        return getCurrentDueDateTime(givenDateTime, getLastMonthDayFromDateTimeAsStringList(givenDateTimeAsStringList), dueDay, reference)
    if isLastMonthDay(dueDay):
        return getCurrentDueDateTime(givenDateTime, closingDay, getLastMonthDayFromDateTimeAsStringList(givenDateTimeAsStringList), reference)
    currentClosingDateTime = getCurrentClosingDateTime(givenDateTime, closingDay, dueDay, reference)
    currentDueDateTime = buildFromDateTimeAsStringList(givenDateTimeAsStringList, dueDay)
    return currentDueDateTime if currentClosingDateTime < currentDueDateTime else nextMonth(currentDueDateTime)


def nextMonth(dateTime):
    if not isLastMonthDateTimeAndIsNotFebruary(dateTime):
        return DateTimeHelper.plusMonths(dateTime, months=1)
    return DateTimeHelper.minusDays(DateTimeHelper.plusMonths(DateTimeHelper.plusDays(dateTime, days=1), months=1), days=1)


def previousMonth(dateTime):
    if not isLastMonthDateTimeAndIsNotFebruary(dateTime):
        return DateTimeHelper.minusMonths(dateTime, months=1)
    return DateTimeHelper.minusDays(DateTimeHelper.minusMonths(DateTimeHelper.plusDays(dateTime, days=1), months=1), days=1)
    

def isLastMonthDateTimeAndIsNotFebruary(dateTime):
    return ObjectHelper.equals(dateTime, buildLastMonthDateTimeFromDateTimeAsStringList(getDateTimeAsStringList(dateTime))) and ObjectHelper.notEquals(28, getDayAsInt(dateTime))


def getNextDueDateTime(givenDateTime, closingDay, dueDay, reference):
    return nextMonth(getCurrentDueDateTime(givenDateTime, closingDay, dueDay, reference))


def getDateTimeAsStringList(givenDateTime):
    return str(str(givenDateTime).split()[0]).split(c.DASH)


def isLastMonthDay(givenDay):
    return 0 > givenDay

def getLastMonthDayFromDateTimeAsStringList(givenDateTimeAsStringList):
    return getDayAsInt(buildLastMonthDateTimeFromDateTimeAsStringList(givenDateTimeAsStringList))

def buildLastMonthDateTimeFromDateTimeAsStringList(dateTimeAsStringList):
    return DateTimeHelper.minusDays(
        DateTimeHelper.plusMonths(
            buildFromDateTimeAsStringList(dateTimeAsStringList, IntervalConstant.FIRST_MONTH_DAY), 
            months = 1
        ),
        days = 1
    )

def buildFromDateTimeAsStringList(dateTimeAsStringList, day):
    return DateTimeHelper.of(
        f'''{dateTimeAsStringList[0]}{
            c.DASH
        }{dateTimeAsStringList[1]}{
            c.DASH
        }{prefixWithZeroIfNeeded(day)}{
            c.SPACE
        }{IntervalConstant.DEFAULT_DUE_TIME}'''
    )


def getDayAsInt(givenDateTime):
    return int(str(givenDateTime).split()[0].split(c.DASH)[-1])


def prefixWithZeroIfNeeded(number):
    return f'{number:0>2}'