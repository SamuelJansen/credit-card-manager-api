class AuthorizedRequest:
    __tablename__ = 'AuthorizedRequest'

    def __init__(self,
        id = None,
        key = None,
        account = None,
        domain = None,
        operation = None,
        resourceKeys = None
    ):
        self.id = id
        self.key = key
        self.account = account
        self.domain = domain
        self.operation = operation
        self.resourceKeys = resourceKeys

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, accountKey={self.account.key}, domain={self.domain}, operation={self.operation}, resourceKeys={self.resourceKeys})'
