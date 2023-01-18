from converter.static import PurchaseStaticConverter


class PurchaseRequestDto:
    def __init__(self,
        key = None,
        creditCardKey = None,
        label = None,
        value = None,
        installments = None,
        purchaseAt = None
    ):
        self.key = key
        self.creditCardKey = creditCardKey
        self.label = label
        self.value = value
        self.installments = installments
        self.purchaseAt = purchaseAt
        PurchaseStaticConverter.overrideDefaultValues(self)


class PurchaseResponseDto:
    def __init__(self,
        key = None,
        creditCardKey = None,
        label = None,
        value = None,
        installments = None,
        purchaseAt = None,
        creditCard = None,
        installmentList = None
    ):
        self.key = key
        self.creditCardKey = creditCardKey
        self.label = label
        self.value = value
        self.installments = installments
        self.purchaseAt = purchaseAt
        self.creditCard = creditCard
        self.installmentList = installmentList
        PurchaseStaticConverter.overrideDefaultValues(self)


class PurchaseQueryDto:
    def __init__(self,
        key = None,
        creditCardKey = None,
        label = None
    ):
        self.key = key
        self.creditCardKey = creditCardKey
        self.label = label
        PurchaseStaticConverter.overrideDefaultQueryValues(self)


class PurchaseQueryAllDto:
    def __init__(self,
        keyList = None,
        creditCardKeyList = None,
        labelList = None
    ):
        self.keyList = keyList
        self.creditCardKeyList = creditCardKeyList
        self.labelList = labelList
        PurchaseStaticConverter.overrideDefaultQueryValues(self)
