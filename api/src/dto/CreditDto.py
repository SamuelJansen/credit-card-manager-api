from converter.static import CreditStaticConverter


class CreditRequestDto:
    def __init__(self,
        key = None,
        limit = None,
        customLimit = None,
        value = None
    ):
        self.key = key
        self.limit = limit
        self.customLimit = customLimit
        self.value = value
        CreditStaticConverter.overrideDefaultValues(self)


class CreditResponseDto:
    def __init__(self,
        key = None,
        limit = None,
        customLimit = None,
        value = None
    ):
        self.key = key
        self.limit = limit
        self.customLimit = customLimit
        self.value = value
        CreditStaticConverter.overrideDefaultValues(self)


class CreditQueryDto:
    def __init__(self,
        key = None
    ):
        self.key = key
        CreditStaticConverter.overrideDefaultQueryValues(self)


class CreditQueryAllDto:
    def __init__(self,
        keyList = None
    ):
        self.keyList = keyList
        CreditStaticConverter.overrideDefaultQueryValues(self)
