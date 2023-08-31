from python_helper import Constant as c
from python_helper import ObjectHelper, DateTimeHelper, log

from constant import IntervalConstant


def getDayAsInt(givenDateTime):
    return int(str(givenDateTime).split()[0].split(c.DASH)[-1])


def prefixWithZeroIfNeeded(number):
    return f'{number:0>2}'


def getCurrentClosingDateTime(givenDateTime, closingDay):
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    if isLastMonthDay(closingDay):
        parsedClosingDay = getDayAsInt(
            DateTimeHelper.minusDays(
                DateTimeHelper.plusMonths(
                    f'''{givenDateTimeAsStringList[0]}{
                        c.DASH
                    }{givenDateTimeAsStringList[1]}{
                        c.DASH
                    }{prefixWithZeroIfNeeded(IntervalConstant.FIRST_MONTH_DAY)}{
                        c.SPACE
                    }{IntervalConstant.DEFAULT_DUE_TIME}''', 
                    months = 1
                ),
                days = 1
            )
        )
        return getCurrentClosingDateTime(givenDateTime, parsedClosingDay)
    return DateTimeHelper.plusMonths(
        DateTimeHelper.of(
            dateTime = f'''{givenDateTimeAsStringList[0]}{
                c.DASH
            }{givenDateTimeAsStringList[1]}{
                c.DASH
            }{prefixWithZeroIfNeeded(closingDay)}{
                c.SPACE
            }{IntervalConstant.DEFAULT_CLOSING_TIME}'''
        ),
        months = 0 if int(givenDateTimeAsStringList[-1]) <= closingDay else 1
    )


def getNextClosingDateTime(givenDateTime, closingDay):
    return DateTimeHelper.plusMonths(
        getCurrentClosingDateTime(givenDateTime, closingDay),
        months = 1
    )


def getCurrentDueDateTime(givenDateTime, closingDay, dueDay):
    givenDateTimeAsStringList = getDateTimeAsStringList(givenDateTime)
    if isLastMonthDay(closingDay):
        parsedClosingDay = getDayAsInt(
            DateTimeHelper.minusDays(
                DateTimeHelper.plusMonths(
                    f'''{givenDateTimeAsStringList[0]}{
                        c.DASH
                    }{givenDateTimeAsStringList[1]}{
                        c.DASH
                    }{prefixWithZeroIfNeeded(IntervalConstant.FIRST_MONTH_DAY)}{
                        c.SPACE
                    }{IntervalConstant.DEFAULT_DUE_TIME}''', 
                    months = 1
                ),
                days = 1
            )
        )
        return getCurrentDueDateTime(givenDateTime, parsedClosingDay, dueDay)
    if isLastMonthDay(dueDay):
        parsedDueDay = getDayAsInt(
            DateTimeHelper.minusDays(
                DateTimeHelper.plusMonths(
                    f'''{givenDateTimeAsStringList[0]}{
                        c.DASH
                    }{givenDateTimeAsStringList[1]}{
                        c.DASH
                    }{prefixWithZeroIfNeeded(IntervalConstant.FIRST_MONTH_DAY)}{
                        c.SPACE
                    }{IntervalConstant.DEFAULT_DUE_TIME}''', 
                    months = 1
                ),
                days = 1
            )
        )
        return getCurrentDueDateTime(givenDateTime, closingDay, parsedDueDay)
    return DateTimeHelper.plusMonths(
        DateTimeHelper.of(
            dateTime = f'''{givenDateTimeAsStringList[0]}{
                c.DASH
            }{givenDateTimeAsStringList[1]}{
                c.DASH
            }{prefixWithZeroIfNeeded(dueDay)}{
                c.SPACE
            }{IntervalConstant.DEFAULT_DUE_TIME}'''
        ),
        months = 0 if closingDay < dueDay and int(givenDateTimeAsStringList[-1]) <= dueDay else 1
    )


def getNextDueDateTime(givenDateTime, closingDay, dueDay):
    return DateTimeHelper.plusMonths(
        getCurrentDueDateTime(givenDateTime, closingDay, dueDay),
        months = 1
    )


def getDateTimeAsStringList(givenDateTime):
    return str(str(givenDateTime).split()[0]).split(c.DASH)


# def getPlusMonsths(givenDay, closingDay, dueDay):
#     log.debugIt(givenDay)
#     log.debugIt(closingDay)
#     log.debugIt(dueDay)
#     log.debugIt(comparrisonDay)
#     # if isLastMonthDay(baseDay) or isLastMonthDay(comparrisonDay):
#     #     if isLastMonthDay(baseDay) and not isLastMonthDay(comparrisonDay):
#     #         return 0
#     #     elif not isLastMonthDay(baseDay) and isLastMonthDay(comparrisonDay):
#     #         return 0
#     if givenDay <= comparrisonDay:
#         return 0 if givenDay <= baseDay else 1 
#     else:
#         return 1 
#     # return 0 if 0 > baseDay or baseDay > givenDay else 1


def isLastMonthDay(givenDay):
    return 0 > givenDay