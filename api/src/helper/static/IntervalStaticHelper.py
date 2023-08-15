from python_helper import Constant as c
from python_helper import DateTimeHelper

from constant import IntervalConstant


def getCurrentClosingDateTime(givenDateTime, closingDay, comparrisonDay):
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    return DateTimeHelper.plusMonths(
        DateTimeHelper.of(
            dateTime = f'''{givenDateTimeAsStringList[0]}{
                c.DASH
            }{givenDateTimeAsStringList[1]}{
                c.DASH
            }{closingDay:02}{
                c.SPACE
            }{IntervalConstant.DEFAULT_CLOSING_TIME}''' if closingDay > 0 else DateTimeHelper.minusDays(
                f'''{givenDateTimeAsStringList[0]}{
                    c.DASH
                }{givenDateTimeAsStringList[1]}{
                    c.DASH
                }{IntervalConstant.FIRST_MONTH_DAY:02}{
                    c.SPACE
                }{IntervalConstant.DEFAULT_CLOSING_TIME}''',
                days = 1
            )
        ),
        months = getPlusMonsths(givenDateTimeAsStringList, comparrisonDay)
    )


def getNextClosingDateTime(givenDateTime, closingDay, comparrisonDay):
    return DateTimeHelper.plusMonths(
        getCurrentClosingDateTime(givenDateTime, closingDay, comparrisonDay),
        months = 1
    )


def getCurrentDueDateTime(givenDateTime, dueDay, comparrisonDay):
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    return DateTimeHelper.plusMonths(
        DateTimeHelper.of(
            dateTime = f'''{givenDateTimeAsStringList[0]}{
                c.DASH
            }{givenDateTimeAsStringList[1]}{
                c.DASH
            }{dueDay:02}{
                c.SPACE
            }{IntervalConstant.DEFAULT_DUE_TIME}''' if dueDay > 0 else DateTimeHelper.minusDays(
                f'''{givenDateTimeAsStringList[0]}{
                    c.DASH
                }{givenDateTimeAsStringList[1]}{
                    c.DASH
                }{IntervalConstant.FIRST_MONTH_DAY:02}{
                    c.SPACE
                }{IntervalConstant.DEFAULT_DUE_TIME}''',
                days = 1
            )
        ),
        months = getPlusMonsths(givenDateTimeAsStringList, comparrisonDay)
    )


def getNextDueDateTime(givenDateTime, dueDay, comparrisonDay):
    return DateTimeHelper.plusMonths(
        getCurrentDueDateTime(givenDateTime, dueDay, comparrisonDay),
        months = 1
    )


def getDateTimeAsStringList(givenDateTime):
    return str(str(givenDateTime).split()[0]).split(c.DASH)


def getPlusMonsths(givenDateTimeAsStringList, comparrisonDay):
    return 0 if 0 > comparrisonDay or comparrisonDay > int(givenDateTimeAsStringList[-1]) else 1