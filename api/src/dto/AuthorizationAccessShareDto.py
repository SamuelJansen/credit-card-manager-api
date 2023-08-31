class AuthorizationAccessShareRequestDto:
    def __init__(self,
        resourceKey = None,
        domain = None,
        operation = None,
        accountKey = None
    ):
        self.resourceKey = resourceKey
        self.domain = domain
        self.operation = operation
        self.accountKey = accountKey


class AuthorizationAccessShareResponseDto:
    def __init__(self,
        resourceKey = None,
        domain = None,
        operation = None,
        accountKey = None
    ):
        self.resourceKey = resourceKey
        self.domain = domain
        self.operation = operation
        self.accountKey = accountKey


class AuthorizationAccessShareAllRequestDto:
    def __init__(self,
        resourceKeyList = None,
        domain = None,
        operationList = None,
        accountKey = None
    ):
        self.resourceKeyList = resourceKeyList
        self.domain = domain
        self.operationList = operationList
        self.accountKey = accountKey


class AuthorizationAccessShareAllResponseDto:
    def __init__(self,
        resourceKeyList = None,
        domain = None,
        operationList = None,
        accountKey = None
    ):
        self.resourceKeyList = resourceKeyList
        self.domain = domain
        self.operationList = operationList
        self.accountKey = accountKey
