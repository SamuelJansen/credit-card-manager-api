import time

from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, AuditoryUtil, Serializer, EnumItem, JwtConstant

from domain import AuthorizationAccount, AuthorizationAccess, AuthorizationOperation
from domain.SecurityContext import SecurityContext
from config import SimpleAccountsConfig
from dto import AuthorizationAccessDto


def buildAccessMemoryKey(resourceKey, accountKey):
    return f'{resourceKey}:{accountKey}'


@Service()
class SecurityService:

    accesses = {}
    loadingAccess = False
    transactionStateChangeAvailable = True
    transactionKeyList = []

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
    
    
    @ServiceMethod()
    def getAuthorizationAccountKey(self):
        return AuditoryUtil.safellyGetCurrentAthentication(securityClass=AuthorizationAccount.AuthorizationAccount, service=self).key


    @ServiceMethod(requestClass=[AuthorizationAccount.AuthorizationAccount])
    def getAccessesByAccount(self, authorizationAccount):
        return [
            access
            for accessMemoryKey, access in self.accesses.items()
            if authorizationAccount.key == access.accountKey
        ]


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessRequestDto]])
    def shareAll(self, dtoList):
        authorizationAccount = self.getAuthorizationAccount()
        for dto in dtoList:
            self.shareResource(dto.resourceKey, dto.domain, dto.operation, dto.accountKey, authorizationAccount)


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessRequestDto]])
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


    def accessesAreLoaded(self):
        return ObjectHelper.isNotEmpty(self.accesses)


    def accessesArentLoaded(self):
        return not self.accessesAreLoaded()


    @ServiceMethod()
    def loadAccessIfNeeded(self):
        log.debug(self.loadAccessIfNeeded, 'Loading authorized accesses proccess called')
        if self.mustLoadAccess():
            self.loadingAccess = True
            self.lockTransactionStateChange()
            try:
                log.debug(self.loadAccessIfNeeded, 'Loadding authorized accesses')
                for access in self.repository.security.readAccesses():
                    self.accesses[buildAccessMemoryKey(access.resourceKey, access.accountKey)] = access
                log.status(self.loadAccessIfNeeded, 'Authorized accesses loaded')
            except Exception as exception:
                log.failure(self.loadAccessIfNeeded, '''Things didn't whent well''', exception=exception)
            self.loadingAccess = False
            self.unlockTransactionStateChange()
        log.debug(self.loadAccessIfNeeded, 'Loading authorized accesses proccess completed')


    @ServiceMethod()
    def overrideRepository(self):
        log.debug(self.overrideRepository, 'Override repository proccess called')
        if self.offTransaction():
            self.awaitLoadingAccessIfNeeded()
            self.lockTransactionStateChange()
            try:
                log.debug(self.overrideRepository, 'Overriding authorized accesses')
                self.repository.security.writeAccesses([*self.accesses.values()])
                log.status(self.overrideRepository, 'Authorized accesses overriden')
            except Exception as exception:
                log.failure(self.overrideRepository, '''Things didn't whent well''', exception=exception)
            self.unlockTransactionStateChange()
        log.debug(self.overrideRepository, 'Override repository proccess completed')


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
        ###- WARNING
        ###- self.lockTransactionIfNeeded(transactionKey) changes self.offTransaction() value
        ###- also, self.loadAccessIfNeeded() takes a lot of time to proccess, therefore its imperative to lock transaction before load access
        if self.offTransaction():
            self.lockTransactionIfNeeded(transactionKey)
            self.loadAccessIfNeeded()
        else:
            self.lockTransactionIfNeeded(transactionKey)
        return transactionKey


    def unlockTransaction(self, transactionKey):
        self.unlockTransactionIfNeeded(transactionKey)
        self.overrideRepository()

    def unlockAllTransactionsDueError(self, transactionKeyError):
        log.prettyJson(self.unlockAllTransactionsDueError, f'Unlocking all transactions due {transactionKeyError} transaction error', self.transactionKeyList, logLevel=log.WARNING)
        for transactionKey in [*self.transactionKeyList]:
            self.unlockTransaction(transactionKey)
        log.warning(self.unlockAllTransactionsDueError, f'All transactions were unlocked due {transactionKeyError} transaction error')
        


    def lockTransactionIfNeeded(self, transactionKey):
        self.awaitLoadingAccessIfNeeded()
        if transactionKey not in self.transactionKeyList:
            self.transactionKeyList.append(transactionKey)
        else:
            log.warning(self.lockTransactionIfNeeded, f'Somehow the {transactionKey} transaction was already starded once (or more)')


    def unlockTransactionIfNeeded(self, transactionKey):
        self.awaitLoadingAccessIfNeeded()
        if transactionKey in self.transactionKeyList:
            self.transactionKeyList.remove(transactionKey)
        else:
            log.warning(self.unlockTransactionIfNeeded, f'Somehow the {transactionKey} transaction was already over or did ended twice (or more)')


    def onTransaction(self):
        return ObjectHelper.isNotEmpty(self.transactionKeyList)


    def offTransaction(self):
        return not self.onTransaction()


    def lockTransactionStateChange(self):
        self.awaitTransactionStateChangeToBeAvailable()
        self.transactionStateChangeAvailable = False


    def unlockTransactionStateChange(self):
        self.transactionStateChangeAvailable = True
    

    def mustLoadAccess(self):
        return self.accessesArentLoaded() and not self.onLoadingAccess()


    def transactionStateChangeIsAvailable(self):
        return True and self.transactionStateChangeAvailable


    def transactionStateChangeIsNotAvailable(self):
        return not self.transactionStateChangeIsAvailable()


    def onLoadingAccess(self):
        return True and self.loadingAccess
    

    def awaitLoadingAccessIfNeeded(self):
        while self.onLoadingAccess():
            time.sleep(0.05)


    def awaitTransactionStateChangeToBeAvailable(self):
        while self.transactionStateChangeIsNotAvailable():
            time.sleep(0.05)


    def getState(self):
        return {
            'mustLoadAccess': self.mustLoadAccess(),
            'accessesCount': len(list(self.accesses.keys())),
            'onTransaction': self.onTransaction(),
            'transactionStateChangeAvailable': self.transactionStateChangeAvailable,
            'transactionStateChangeIsNotAvailable': self.transactionStateChangeIsNotAvailable(),
            'transactionKeyList': self.transactionKeyList,
            'loadingAccess': self.loadingAccess,
            'onLoadingAccess': self.onLoadingAccess()
        }