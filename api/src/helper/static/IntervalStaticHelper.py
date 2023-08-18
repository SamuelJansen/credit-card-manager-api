from python_helper import Constant as c
from python_helper import ObjectHelper, DateTimeHelper, log

from constant import IntervalConstant


def getCurrentClosingDateTime(givenDateTime, closingDay, comparrisonDay):
    # log.debug(getCurrentClosingDateTime, f'givenDateTime: {givenDateTime}')
    # log.debugIt(closingDay)
    # log.debugIt(comparrisonDay)
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    return DateTimeHelper.plusMonths(
        DateTimeHelper.of(
            dateTime = f'''{givenDateTimeAsStringList[0]}{
                c.DASH
            }{givenDateTimeAsStringList[1]}{
                c.DASH
            }{closingDay:02}{
                c.SPACE
            }{IntervalConstant.DEFAULT_CLOSING_TIME}''' if 0 < closingDay else DateTimeHelper.minusDays(
                DateTimeHelper.plusMonths(
                    f'''{givenDateTimeAsStringList[0]}{
                        c.DASH
                    }{givenDateTimeAsStringList[1]}{
                        c.DASH
                    }{IntervalConstant.FIRST_MONTH_DAY:02}{
                        c.SPACE
                    }{IntervalConstant.DEFAULT_CLOSING_TIME}''',
                    months = 1
                ),
                days = 1
            )
        ),
        months = getPlusMonsths(givenDateTimeAsStringList, closingDay, comparrisonDay)
    )


def getNextClosingDateTime(givenDateTime, closingDay, comparrisonDay):
    # log.debug(getNextClosingDateTime, f'givenDateTime: {givenDateTime}')
    # log.debugIt(closingDay)
    # log.debugIt(comparrisonDay)
    return DateTimeHelper.plusMonths(
        getCurrentClosingDateTime(givenDateTime, closingDay, comparrisonDay),
        months = 1
    )


def getCurrentDueDateTime(givenDateTime, dueDay, comparrisonDay):
    # log.debug(getCurrentDueDateTime, f'givenDateTime: {givenDateTime}')
    # log.debugIt(dueDay)
    # log.debugIt(comparrisonDay)
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    return DateTimeHelper.plusMonths(
        DateTimeHelper.of(
            dateTime = f'''{givenDateTimeAsStringList[0]}{
                c.DASH
            }{givenDateTimeAsStringList[1]}{
                c.DASH
            }{dueDay:02}{
                c.SPACE
            }{IntervalConstant.DEFAULT_DUE_TIME}''' if 0 < dueDay else DateTimeHelper.minusDays(
                DateTimeHelper.plusMonths(
                    f'''{givenDateTimeAsStringList[0]}{
                        c.DASH
                    }{givenDateTimeAsStringList[1]}{
                        c.DASH
                    }{IntervalConstant.FIRST_MONTH_DAY:02}{
                        c.SPACE
                    }{IntervalConstant.DEFAULT_DUE_TIME}''', 
                    months = 1
                ),
                days = 1
            )
        ),
        months = getPlusMonsths(givenDateTimeAsStringList, dueDay, comparrisonDay)
    )


def getNextDueDateTime(givenDateTime, dueDay, comparrisonDay):
    # log.debug(getNextDueDateTime, f'givenDateTime: {givenDateTime}')
    # log.debugIt(dueDay)
    # log.debugIt(comparrisonDay)
    return DateTimeHelper.plusMonths(
        getCurrentDueDateTime(givenDateTime, dueDay, comparrisonDay),
        months = 1
    )


def getDateTimeAsStringList(givenDateTime):
    return str(str(givenDateTime).split()[0]).split(c.DASH)


def getPlusMonsths(givenDateTimeAsStringList, baseDay, comparrisonDay):
    # log.debugIt(givenDateTimeAsStringList)
    # log.debugIt(comparrisonDay)
    # log.debugIt(baseDay)
    if isLastMonthDay(baseDay) or isLastMonthDay(comparrisonDay):
        if isLastMonthDay(baseDay) and not isLastMonthDay(comparrisonDay):
            return 0
        elif not isLastMonthDay(baseDay) and isLastMonthDay(comparrisonDay):
            return 0
    return 0 if 0 > comparrisonDay or comparrisonDay > int(givenDateTimeAsStringList[-1]) else 1


def isLastMonthDay(givenDay):
    return 0 > givenDay