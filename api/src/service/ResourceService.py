from python_framework import Service, ServiceMethod

from dto import AuthorizationAccessShareDto, CreditCardDto, PurchaseDto


@Service()
class ResourceService:


    @ServiceMethod(requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]])
    def shareAllCreditCard(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList = [dto.resourceKey]))
            for creditCardResponseDto in creditCardResponseDtoList:
                self.service.security.shareResource(creditCardResponseDto.credit.key, 'Credit', dto.operation, dto.accountKey, authorizationAccount)
                self.service.security.shareResource(creditCardResponseDto.key, 'CreditCard', dto.operation, dto.accountKey, authorizationAccount)
                if shareRelatedDomains:
                    self.shareAllPurchase(
                        [
                            AuthorizationAccessShareDto.AuthorizationAccessShareAllRequestDto(
                                resourceKeyList = [
                                    purchaseResponseDto.key 
                                    for purchaseResponseDto in self.service.purchase.findAllByQuery(
                                        PurchaseDto.PurchaseQueryAllDto(creditCardKeyList = [creditCardResponseDto.key])
                                    )
                                ],
                                domain = dto.domain,
                                operationList = [dto.operation],
                                accountKey = dto.accountKey
                            )
                        ],
                        shareRelatedDomains = False
                    )
        self.service.security.unlockTransaction(transactionKey)


    @ServiceMethod(requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareAllRequestDto]])
    def shareAllPurchase(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = dto.resourceKeyList))
            if shareRelatedDomains:
                for creditCardKey in list(set([purchaseResponseDto.creditCardKey for purchaseResponseDto in purchaseResponseDtoList])):
                    self.shareAllCreditCard(
                        [
                            AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto(
                                resourceKey = creditCardKey,
                                domain = dto.domain,
                                operation = operation,
                                accountKey = dto.accountKey
                            )
                            for operation in dto.operationList
                        ], 
                        shareRelatedDomains = False
                    )
            for purchaseResponseDto in purchaseResponseDtoList:
                for installmentResponseDto in purchaseResponseDto.installmentList:
                    for operation in dto.operationList:
                        self.service.security.shareResource(installmentResponseDto.key, 'Installment', operation, dto.accountKey, authorizationAccount)
                for operation in dto.operationList:
                    self.service.security.shareResource(purchaseResponseDto.key, 'Purchase', operation, dto.accountKey, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)


    @ServiceMethod(requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareAllRequestDto]])
    def transferAllPurchase(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = dto.resourceKeyList))
            if shareRelatedDomains:
                for creditCardKey in list(set([purchaseResponseDto.creditCardKey for purchaseResponseDto in purchaseResponseDtoList])):
                    self.shareAllCreditCard(
                        [
                            AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto(
                                resourceKey = creditCardKey,
                                domain = dto.domain,
                                operation = operation,
                                accountKey = dto.accountKey
                            )
                            for operation in dto.operationList
                        ], 
                        shareRelatedDomains = False
                    )
            for purchaseResponseDto in purchaseResponseDtoList:
                for installmentResponseDto in purchaseResponseDto.installmentList:
                    for operation in dto.operationList:
                        self.service.security.shareResource(installmentResponseDto.key, 'Installment', operation, dto.accountKey, authorizationAccount)
                self.service.security.revokeResourceAccess(installmentResponseDto.key, authorizationAccount.key, authorizationAccount)
                for operation in dto.operationList:
                    self.service.security.shareResource(purchaseResponseDto.key, 'Purchase', operation, dto.accountKey, authorizationAccount)
                self.service.security.revokeResourceAccess(purchaseResponseDto.key, authorizationAccount.key, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)
