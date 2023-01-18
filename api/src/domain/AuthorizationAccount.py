from python_helper import ObjectHelper
from python_framework import StaticConverter, Serializer


from enumeration.AuthorizationAccountStatus import AuthorizationAccountStatus


class AuthorizationAccount:
    __tablename__ = 'AuthorizationAccount'

    def __init__(self,
        id = None,
        key = None,
        name = None,
        firstName = None,
        lastName = None,
        email = None,
        pictureUrl = None,
        status = None,
        roles = None,
        accesses = None
    ):
        self.id = id
        self.key = StaticConverter.getValueOrDefault(key, Serializer.newUuidAsString())
        self.name = name
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.pictureUrl = pictureUrl
        self.status = AuthorizationAccountStatus.map(StaticConverter.getValueOrDefault(status, AuthorizationAccountStatus.NONE))
        self.roles = StaticConverter.getValueOrDefault(roles, [])
        self.accesses = StaticConverter.getValueOrDefault(accesses, [])

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, name={self.name}, email={self.email}, status=({self.status}), roles={self.roles})'

    def getAccessesByDomainAndOperation(self, requestedDomain, requestedOperation):
        return [] if ObjectHelper.isNone(requestedOperation) else [
            access
            for access in self.accesses
            if (
                ObjectHelper.equals(access.domain, requestedDomain) and
                requestedOperation in access.operations and
                ObjectHelper.equals(access.accountKey, self.key)
            )
        ]

    def getOperationsByDomainAndResourceKey(self, requestedDomain, requestedResourceKey):
        return [] if ObjectHelper.isNone(requestedResourceKey) else ObjectHelper.flatMap([
            access.operations
            for access in self.accesses
            if (
                ObjectHelper.equals(access.domain, requestedDomain) and
                ObjectHelper.equals(access.resourceKey, requestedResourceKey) and
                ObjectHelper.equals(access.accountKey, self.key)
            )
        ])

    def getResourceKeysByDomainAndOperation(self, requestedDomain, requestedOperation):
        return [
            access.resourceKey
            for access in self.accesses
            if (
                ObjectHelper.equals(access.domain, requestedDomain) and
                requestedOperation in access.operations and
                ObjectHelper.equals(access.accountKey, self.key)
            )
        ]
