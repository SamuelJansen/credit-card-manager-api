from converter.static import DefaultStaticConverter
from python_helper import DateTimeHelper, ObjectHelper

class InvoiceRequestDto:
    def __init__(self,
        key = None
    ):
        self.key = key
        DefaultStaticConverter.overrideDefaultValues(self)


class InvoiceResponseDto:
    def __init__(self,
        key = None,
        value = None,
        installmentList = None,
        creditCard = None,
        closeAt = None,
        dueAt = None
    ):
        self.key = key
        self.value = value
        self.installmentList = installmentList
        self.creditCard = creditCard
        self.closeAt = DateTimeHelper.dateNow() if ObjectHelper.isNone(closeAt) else DateTimeHelper.dateOf(dateTime=DateTimeHelper.of(date=closeAt))
        self.dueAt = DateTimeHelper.dateNow() if ObjectHelper.isNone(dueAt) else DateTimeHelper.dateOf(dateTime=DateTimeHelper.of(date=dueAt))
        DefaultStaticConverter.overrideDefaultValues(self)


class InvoiceQueryDto:
    def __init__(self,
        keyList = None,
        creditCardKeyList = None,
        date = None
    ):
        self.keyList = keyList
        self.creditCardKeyList = creditCardKeyList
        self.date = DateTimeHelper.dateNow() if ObjectHelper.isNone(date) else DateTimeHelper.dateOf(dateTime=DateTimeHelper.of(date=date))
        DefaultStaticConverter.overrideDefaultQueryValues(self)
