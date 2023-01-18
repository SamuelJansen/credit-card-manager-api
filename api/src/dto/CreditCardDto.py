from converter.static import CreditCardStaticConverter

    
class CreditCardRequestDto:
    def __init__(self,
        key = None,
        creditKey = None,
        label = None,
        customLimit = None,
        value = None,
        expirationDate = None,
        closingDay = None,
        dueDay = None
    ):
        self.key = key
        self.creditKey = creditKey
        self.label = label
        self.customLimit = customLimit
        self.value = value
        self.expirationDate = expirationDate
        self.closingDay = closingDay
        self.dueDay = dueDay
        CreditCardStaticConverter.overrideDefaultValues(self)


class CreditCardResponseDto:
    def __init__(self,
        key = None,
        creditKey = None,
        label = None,
        customLimit = None,
        value = None,
        expirationDate = None,
        closingDay = None,
        dueDay = None,
        credit = None
    ):
        self.key = key
        self.creditKey = creditKey
        self.label = label
        self.customLimit = customLimit
        self.value = value
        self.expirationDate = expirationDate
        self.closingDay = closingDay
        self.dueDay = dueDay
        self.credit = credit
        CreditCardStaticConverter.overrideDefaultValues(self)


class CreditCardQueryDto:
    def __init__(self,
        key = None,
        creditKey = None,
        expirationDate = None,
        closingDay = None,
        dueDay = None
    ):
        self.key = key
        self.creditKey = creditKey
        self.expirationDate = expirationDate
        self.closingDay = closingDay
        self.dueDay = dueDay
        CreditCardStaticConverter.overrideDefaultQueryValues(self)


class CreditCardQueryAllDto:
    def __init__(self,
        keyList = None,
        creditKeyList = None,
        labelList = None,
        expirationDate = None,
        closingDay = None,
        dueDay = None
    ):
        self.keyList = keyList
        self.creditKeyList = creditKeyList
        self.labelList = labelList
        self.expirationDate = expirationDate
        self.closingDay = closingDay
        self.dueDay = dueDay
        CreditCardStaticConverter.overrideDefaultQueryValues(self)
