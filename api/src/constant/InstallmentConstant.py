from python_helper import DateTimeHelper

from constant import IntervalConstant
from constant import PurchaseConstant
from enumeration.InstallmentStatus import InstallmentStatus


YEARS_AHEAD = 10
TIME_NOW = DateTimeHelper.timeNow()
DATE_NOW = DateTimeHelper.dateNow()
DATE_AHEAD = DateTimeHelper.dateOf(
    dateTime = DateTimeHelper.forcedlyParse(f'{DATE_NOW.year + YEARS_AHEAD}-{DATE_NOW.month:02}-{DATE_NOW.day:02} {TIME_NOW}')
)

DEFAULT_VALUE = 0.0
DEFAULT_ORDER = 0
DEFAULT_INSTALLMENTS = PurchaseConstant.DEFAULT_INSTALLMENTS
DEFAULT_STATUS = InstallmentStatus.NONE

FIRST_MONTH_DAY = IntervalConstant.FIRST_MONTH_DAY
DEFAULT_DUE_TIME = IntervalConstant.DEFAULT_DUE_TIME
DEFAULT_CLOSING_TIME = IntervalConstant.DEFAULT_CLOSING_TIME

MIN_START_DATE_TIME = DateTimeHelper.forcedlyParse('1969-01-01 00:00:01.000')
MAX_END_DATE_TIME = DateTimeHelper.of(date=DATE_AHEAD, time=TIME_NOW) ###- DateTimeHelper.forcedlyParse('2999-12-31 23:59:59.999')

FROM_DATE_TIME_QUERY_KEY = 'fromDateTime'
TO_DATE_TIME_QUERY_KEY = 'toDateTime'

DATE_TIME_QUERY_KEY_LIST = [
    FROM_DATE_TIME_QUERY_KEY,
    TO_DATE_TIME_QUERY_KEY
]

CREDIT_CARD_KEY = 'creditCardKey'
CREDIT_CARD_KEY_LIST = 'creditCardKeyList'
CREDIT_CARD_QUERY_KEY_LIST = [
    CREDIT_CARD_KEY,
    CREDIT_CARD_KEY_LIST
]

COUNTABLE_TYPES = [
    InstallmentStatus.SCHEADULED,
    InstallmentStatus.PROCESSING,
    InstallmentStatus.PROCESSED
]

PROCCESSABLE_STATUS = [
    InstallmentStatus.CREATED,
    InstallmentStatus.SCHEADULED
]

REVERTABLE_STATUS = [
    InstallmentStatus.PROCESSED
]

SORTTING_ATTRIBUTE = 'installmentAt'