from python_helper import Test, log, ObjectHelper, DateTimeHelper
from api.src.helper.static import IntervalStaticHelper
from api.src.constant import IntervalConstant


TEST_SETTINGS = {}


def getYear(dateTime):
    return str(dateTime).split('-')[0]


def getMonth(dateTime):
    return str(dateTime).split('-')[1]


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def prefixWithZeroIfNeeded():
    #arrange
    dayOneAsInt = 1
    dayOneAsIntAExpected = '01'
    dayTenAsInt = 10
    dayTenAsIntAExpected = '10'

    #act
    dayOneAsIntToAssert = IntervalStaticHelper.prefixWithZeroIfNeeded(dayOneAsInt)
    dayTenAsIntToAssert = IntervalStaticHelper.prefixWithZeroIfNeeded(dayTenAsInt)

    #assert
    assert ObjectHelper.equals(dayOneAsIntAExpected, dayOneAsIntToAssert), f'{dayOneAsIntAExpected} == {dayOneAsIntToAssert}'
    assert ObjectHelper.equals(dayTenAsIntAExpected, dayTenAsIntToAssert), f'{dayTenAsIntAExpected} == {dayTenAsIntToAssert}'


#################################################################
###- current closing - closingDay_20_dueDay_12 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_closingDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_closingDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_closingDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- next closing - closingDay_20_dueDay_12 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_closingDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_closingDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_closingDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'



















#################################################################
###- current closing - closingDay_20_dueDay_12 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_09_10_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-10 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_09_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- next closing - closingDay_20_dueDay_12 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_dueDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_dueDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_dueDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_dueDay_reference_2023_09_10_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-10 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextClosingDateTime_when_dueDay_reference_2023_09_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-20 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'
























#################################################################
###- current due - closingDay_20_dueDay_22 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_15_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_20_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_22_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-22 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_24_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- next due - closingDay_20_dueDay_22 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_15_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_20_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_22_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-22 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_24_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'

























#################################################################
###- current due - closingDay_20_dueDay_22 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_15_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_20_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_22_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-22 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_24_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- next due - closingDay_20_dueDay_22 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_15_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_20_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_22_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-22 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_24_closingDay_20_dueDay_22():
    #arrange
    closingDay = 20 
    dueDay = 22
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-22 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'

























#################################################################
###- current due - closingDay_20_dueDay_12 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_10_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-10 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_12_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-12 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- next due - closingDay_20_dueDay_12 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_10_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-10 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_12_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-12 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_closingDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'

























#################################################################
###- current due - closingDay_20_dueDay_12 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_10_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-10 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_12_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-12 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- next due - closingDay_20_dueDay_12 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_10_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-10 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_12_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-12 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_15_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-15 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_20_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-20 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getNextDueDateTime_when_dueDay_reference_2023_08_24_closingDay_20_dueDay_12():
    #arrange
    closingDay = 20 
    dueDay = 12
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-08-24 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-12 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getNextDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'























#################################################################
###- current closing - 2023-09-01 closingDay_31_dueDay_15 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_closingDay_reference_2023_09_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-30 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- current closing - 2023-09-01 closingDay_31_dueDay_15 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_09_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-31 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_09_01_h0701_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-01 07:01:00.000')
    expected = DateTimeHelper.of(f'''2023-08-31 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- current due - 2023-09-01 closingDay_31_dueDay_15 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_09_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-10-15 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- current due - 2023-09-01 closingDay_31_dueDay_15 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_09_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-09-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-09-15 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'























#################################################################
###- current closing - 2023-07-01 closingDay_31_dueDay_15 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_closingDay_reference_2023_07_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-07-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-07-31 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- current closing - 2023-07-01 closingDay_31_dueDay_15 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentClosingDateTime_when_dueDay_reference_2023_07_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-07-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-06-30 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentClosingDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- current due - 2023-07-01 closingDay_31_dueDay_15 CLOSING_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_closingDay_reference_2023_07_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.CLOSING_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-07-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-08-15 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'


#################################################################
###- current due - 2023-07-01 closingDay_31_dueDay_15 DUE_DAY_REFERENCE
#################################################################


@Test(
    environmentVariables={
        log.ENABLE_LOGS_WITH_COLORS : True
    },
    **TEST_SETTINGS
)
def getCurrentDueDateTime_when_dueDay_reference_2023_07_01_closingDay_31_dueDay_15():
    #arrange
    closingDay = -1 
    dueDay = 15
    reference = IntervalConstant.DUE_DAY_REFERENCE
    dateTime = DateTimeHelper.of('2023-07-01 14:59:00.000')
    expected = DateTimeHelper.of(f'''2023-07-15 {DateTimeHelper.DEFAULT_TIME_END}''')

    #act
    toAssert = IntervalStaticHelper.getCurrentDueDateTime(dateTime, closingDay, dueDay, reference)

    #assert
    assert ObjectHelper.equals(expected, toAssert), f'{expected} == {toAssert}'