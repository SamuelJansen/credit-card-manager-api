from converter.static import InstallmentStaticConverter


class InstallmentRequestDto:
    def __init__(self,
        key = None,
        purchaseKey = None,
        label = None,
        value = None,
        installmentAt = None,
        installments = None,
        order = None,
        status = None
    ):
        self.key = key
        self.purchaseKey = purchaseKey
        self.label = label
        self.value = value
        self.installmentAt = installmentAt
        self.installments = installments
        self.order = order
        self.status = status
        InstallmentStaticConverter.overrideDefaultValues(self)


class InstallmentResponseDto:
    def __init__(self,
        key = None,
        purchaseKey = None,
        label = None,
        value = None,
        installmentAt = None,
        installments = None,
        order = None,
        status = None,
        purchase = None
    ):
        self.key = key
        self.purchaseKey = purchaseKey
        self.label = label
        self.value = value
        self.installmentAt = installmentAt
        self.installments = installments
        self.order = order
        self.status = status
        self.purchase = purchase
        InstallmentStaticConverter.overrideDefaultValues(self)


class InstallmentQueryDto:
    def __init__(self,
        key = None,
        purchaseKey = None,
        label = None,
        status = None,
        fromDateTime = None,
        toDateTime = None,
        creditCardKey = None
    ):
        self.key = key
        self.purchaseKey = purchaseKey
        self.label = label
        self.status = status
        self.fromDateTime = fromDateTime
        self.toDateTime = toDateTime
        self.creditCardKey = creditCardKey
        InstallmentStaticConverter.overrideDefaultQueryValues(self)


class InstallmentQueryAllDto:
    def __init__(self,
        keyList = None,
        purchaseKeyList = None,
        labelList = None,
        statusList = None,
        fromDateTime = None,
        toDateTime = None,
        creditCardKeyList = None
    ):
        self.keyList = keyList
        self.purchaseKeyList = purchaseKeyList
        self.labelList = labelList
        self.statusList = statusList
        self.fromDateTime = fromDateTime
        self.toDateTime = toDateTime
        self.creditCardKeyList = creditCardKeyList
        InstallmentStaticConverter.overrideDefaultQueryValues(self)
