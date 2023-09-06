class AuthorizationAccessRequestDto:
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


class AuthorizationAccessResponseDto:
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


class AuthorizationAccessAllRequestDto:
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


class AuthorizationAccessAllResponseDto:
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
