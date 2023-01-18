from converter.static import AuthorizationStaticConverter


class RequestedAuthorization:
    __tablename__ = 'RequestedAuthorization'

    def __init__(self,
        id = None,
        key = None,
        resourceKeys = None,
        domain = None,
        operation = None
    ):
        self.id = id
        self.key = key
        self.resourceKeys = resourceKeys
        self.domain = domain
        self.operation = operation
        AuthorizationStaticConverter.overrideDefaultValues(self)

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, resourceKeys={self.resourceKeys}, domain={self.domain}, operation={self.operation})'
