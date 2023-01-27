from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, AuditoryUtil, Serializer, EnumItem, JwtConstant

from domain import AuthorizationAccount, AuthorizationAccess, AuthorizationOperation
from domain.SecurityContext import SecurityContext
from config import SimpleAccountsConfig
from dto import AuthorizationAccessShareDto


def buildAccessMemoryKey(resourceKey, accountKey):
    return f'{resourceKey}:{accountKey}'


@Service()
class SecurityService:

    accesses = {}
    transactionKey = None

    @ServiceMethod()
    def getAuthorizationAccount(self):
        authorizationAccount = AuditoryUtil.safellyGetCurrentAthentication(securityClass=AuthorizationAccount.AuthorizationAccount, service=self)
        securityContextItemsAsString = SecurityContext.getItemsAsString()
        authorizationAccount.key = authorizationAccount._contextInfo.get(JwtConstant.KW_IDENTITY)
        authorizationAccount.roles = [
            SecurityContext.map(role)
            for role in authorizationAccount._contextInfo.get(JwtConstant.KW_CONTEXT)
            if role in securityContextItemsAsString
        ]
        authorizationAccount.accesses = self.getAccessesByAccount(authorizationAccount)
        ###- log.prettyJson(self.getAuthorizationAccount, 'Authorization account', Serializer.getObjectAsDictionary(authorizationAccount), logLevel=log.DEBUG)
        return authorizationAccount


    @ServiceMethod(requestClass=[AuthorizationAccount.AuthorizationAccount])
    def getAccessesByAccount(self, authorizationAccount):
        return [
            access
            for accessMemoryKey, access in self.accesses.items()
            if authorizationAccount.key == access.accountKey
        ]


    @ServiceMethod(requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]])
    def shareAll(self, dtoList):
        authorizationAccount = self.getAuthorizationAccount()
        for dto in dtoList:
            self.shareResource(dto.resourceKey, dto.domain, dto.operation, dto.accountKey, authorizationAccount)


    @ServiceMethod(requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]])
    def revokeAll(self, dtoList):
        authorizationAccount = self.getAuthorizationAccount()
        for dto in dtoList:
            accessMemoryKey = self.revokeResourceAccess(dto.resourceKey, dto.accountKey, authorizationAccount)


    def createOrUpdateOrDeleteAccesses(self, resourceKeys, domain, operation):
        authorizationAccount = self.getAuthorizationAccount()
        for resourceKey in resourceKeys:
            accessMemoryKey = buildAccessMemoryKey(resourceKey, authorizationAccount.key)
            if AuthorizationOperation.DELETE == operation and accessMemoryKey in self.accesses:
                self.deleteAccesses(accessMemoryKey, resourceKey, domain, operation, authorizationAccount)
            elif accessMemoryKey not in self.accesses:
                self.createAccess(accessMemoryKey, resourceKey, domain, operation, authorizationAccount)
            else:
                self.updateAccess(accessMemoryKey, resourceKey, domain, operation, authorizationAccount)


    def createAccess(self, accessMemoryKey, resourceKey, domain, operation, authorizationAccount):
        self.accesses[accessMemoryKey] = AuthorizationAccess.AuthorizationAccess(
            accountKey = authorizationAccount.key,
            resourceKey = resourceKey,
            operations = [],
            domain = domain
        )
        if operation in AuthorizationOperation.WRITTING_OPERATIONS:
            if AuthorizationOperation.POST == operation:
                self.accesses[accessMemoryKey].operations = [
                    *AuthorizationOperation.READDING_OPERATIONS,
                    *AuthorizationOperation.WRITTING_OPERATIONS
                ]
            if AuthorizationOperation.PUT == operation:
                self.accesses[accessMemoryKey].operations = [
                    AuthorizationOperation.GET,
                    AuthorizationOperation.PUT,
                    AuthorizationOperation.DELETE
                ]
        elif operation in AuthorizationOperation.READDING_OPERATIONS:
            self.accesses[accessMemoryKey].operations = [
                *AuthorizationOperation.READDING_OPERATIONS
            ]
        ###- log.prettyJson(self.createAccess, 'Access created', self.accesses[accessMemoryKey], logLevel=log.DEBUG)


    def updateAccess(self, accessMemoryKey, resourceKey, domain, operation, authorizationAccount):
        if accessMemoryKey in self.accesses:
            if operation in AuthorizationOperation.WRITTING_OPERATIONS:
                if AuthorizationOperation.POST == operation:
                    self.accesses[accessMemoryKey].operations = [
                        *AuthorizationOperation.READDING_OPERATIONS,
                        *AuthorizationOperation.WRITTING_OPERATIONS
                    ]
                elif AuthorizationOperation.PUT == operation:
                    for op in [
                        *AuthorizationOperation.READDING_OPERATIONS,
                        *AuthorizationOperation.WRITTING_OPERATIONS
                    ]:
                        if not AuthorizationOperation.POST == operation and op not in self.accesses[accessMemoryKey].operations:
                            self.accesses[accessMemoryKey].operations.append(op)
            if operation not in self.accesses[accessMemoryKey].operations:
                self.accesses[accessMemoryKey].operations.append(operation)
            ###- log.prettyJson(self.updateAccess, 'Access updated', self.accesses[accessMemoryKey], logLevel=log.DEBUG)
        else:
            ###- log.failure(self.updateAccess, f'Access not updated. The memmory access key {accessMemoryKey} does not exists', exception=None)
            ...


    def deleteAccesses(self, accessMemoryKey, resourceKey, domain, operation, authorizationAccount):
        if accessMemoryKey in self.accesses and AuthorizationOperation.DELETE in self.accesses[accessMemoryKey].operations:
            for access in [
                access
                for access in [*self.accesses.values()]
                if access.resourceKey == resourceKey
            ]:
                deletedAccess = self.accesses.pop(buildAccessMemoryKey(access.resourceKey, access.accountKey))
                ###- log.prettyJson(self.deleteAccesses, 'Access revoked', deletedAccess, logLevel=log.DEBUG)


    def shareResource(self, resourceKey, domain, operation, accountKeyToShare, authorizationAccount):
        if buildAccessMemoryKey(resourceKey, authorizationAccount.key) in self.accesses:
            accessMemoryKey = buildAccessMemoryKey(resourceKey, accountKeyToShare)
            if accessMemoryKey not in self.accesses:
                self.createAccess(
                    accessMemoryKey,
                    resourceKey,
                    domain,
                    operation,
                    AuthorizationAccount.AuthorizationAccount(key=accountKeyToShare)
                )
            else:
                self.updateShareResource(resourceKey, domain, operation, accountKeyToShare, authorizationAccount)


    def updateShareResource(self, resourceKey, domain, operation, accountKeyToShare, authorizationAccount):
        if buildAccessMemoryKey(resourceKey, authorizationAccount.key) in self.accesses:
            self.updateAccess(
                buildAccessMemoryKey(resourceKey, accountKeyToShare),
                resourceKey,
                domain,
                operation,
                AuthorizationAccount.AuthorizationAccount(key=accountKeyToShare)
            )


    def revokeResourceAccess(self, resourceKey, accountKeyToRevoke, authorizationAccount):
        accessMemoryKey = buildAccessMemoryKey(resourceKey, authorizationAccount.key)
        if accessMemoryKey in self.accesses:
            accessMemoryKeyToRevoke = buildAccessMemoryKey(resourceKey, accountKeyToRevoke)
            if accessMemoryKeyToRevoke in self.accesses:
                revokedResourceAccess = self.accesses.pop(accessMemoryKeyToRevoke)
                ###- log.prettyJson(self.revokeResourceAccess, 'Access revoked', revokedResourceAccess, logLevel=log.DEBUG)


    @ServiceMethod()
    def loadAccessIfNeeded(self):
        if ObjectHelper.isEmpty(self.accesses):
            log.debug(self.overrideRepository, 'Loadding authorized accesses')
            for access in self.repository.security.readAccesses():
                self.accesses[buildAccessMemoryKey(access.resourceKey, access.accountKey)] = access
            log.status(self.overrideRepository, 'Authorized accesses loaded')


    @ServiceMethod()
    def overrideRepository(self):
        if self.offTransaction():
            log.debug(self.overrideRepository, 'Overriding authorized accesses')
            self.repository.security.writeAccesses([*self.accesses.values()])
            log.status(self.overrideRepository, 'Authorized accesses overriden')


    @ServiceMethod()
    def isAdmin(self):
        return self.isAdminDomain(self.getAuthorizationAccount())


    @ServiceMethod()
    def isUser(self):
        return self.isUserDomain(self.getAuthorizationAccount())


    @ServiceMethod(requestClass=[AuthorizationAccount.AuthorizationAccount])
    def isAdminDomain(self, authorizationAccount):
        return self.containsRole(SecurityContext.CREDIT_CARD_ADMIN, authorizationAccount)


    @ServiceMethod(requestClass=[AuthorizationAccount.AuthorizationAccount])
    def isUserDomain(self, authorizationAccount):
        return self.containsRole(SecurityContext.CREDIT_CARD_USER, authorizationAccount)


    @ServiceMethod(requestClass=[EnumItem, AuthorizationAccount.AuthorizationAccount])
    def containsRole(self, role, authorizationAccount):
        return role in authorizationAccount.roles


    def lockTransaction(self):
        transactionKey = Serializer.newUuidAsString()
        if self.offTransaction():
            self.loadAccessIfNeeded()
            self.transactionKey = transactionKey
        return transactionKey


    def unlockTransaction(self, transactionKey):
        if self.onTransaction() and ObjectHelper.equals(self.transactionKey, transactionKey):
            self.transactionKey = None
        self.overrideRepository()


    def onTransaction(self):
        return ObjectHelper.isNotNone(self.transactionKey)


    def offTransaction(self):
        return not self.onTransaction()
