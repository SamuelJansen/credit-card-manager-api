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
