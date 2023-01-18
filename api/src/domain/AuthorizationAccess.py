from python_framework import StaticConverter, Serializer


class AuthorizationAccess:
    __tablename__ = 'AuthorizationAccess'

    def __init__(self,
        id = None,
        key = None,
        accountKey = None,
        resourceKey = None,
        domain = None,
        operations = None
    ):
        self.id = id
        self.key = StaticConverter.getValueOrDefault(key, Serializer.newUuidAsString())
        self.accountKey = accountKey
        self.resourceKey = resourceKey
        self.domain = domain
        self.operations = operations

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, accountKey={self.accountKey}, resourceKey={self.resourceKey}, domain={self.domain}, operations={self.operations})'
