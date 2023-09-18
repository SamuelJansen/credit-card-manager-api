from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod

from dto import AuthorizationAccessDto, CreditCardDto, PurchaseDto


@Service()
class ResourceService:


    @ServiceMethod(requestClass=[CreditCardDto.CreditCardResponseDto])
    def getPurchases(self, creditCardResponseDto):
        try:
            return self.service.purchase.findAllByQuery(
                PurchaseDto.PurchaseQueryAllDto(creditCardKeyList = [creditCardResponseDto.key])
            )
        except:
            return []


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]])
    def shareAllCreditCard(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList = dto.resourceKeyList))
            for creditCardResponseDto in creditCardResponseDtoList:
                for operation in dto.operationList:
                    self.service.security.shareResource(creditCardResponseDto.credit.key, 'Credit', operation, dto.accountKey, authorizationAccount)
                    self.service.security.shareResource(creditCardResponseDto.key, 'CreditCard', operation, dto.accountKey, authorizationAccount)
            if shareRelatedDomains:
                resourceKeyList = list(set([
                    purchaseResponseDto.key 
                    for innerCreditCardResponseDto in creditCardResponseDtoList
                    for purchaseResponseDto in self.getPurchases(innerCreditCardResponseDto)
                ]))
                if ObjectHelper.isNotEmpty(resourceKeyList):
                    self.shareAllPurchase(
                        [
                            AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                resourceKeyList = [*resourceKeyList],
                                domain = dto.domain,
                                operationList = [*dto.operationList],
                                accountKey = dto.accountKey
                            )
                        ],
                        shareRelatedDomains = False
                    )
        self.service.security.unlockTransaction(transactionKey)


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]])
    def shareAllPurchase(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            if ObjectHelper.isNotEmpty(dto.resourceKeyList):
                purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = dto.resourceKeyList))
                if shareRelatedDomains:
                    self.shareAllCreditCard(
                        [
                            AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                resourceKeyList = list(set([purchaseResponseDto.creditCardKey for purchaseResponseDto in purchaseResponseDtoList])),
                                domain = dto.domain,
                                operationList = dto.operationList,
                                accountKey = dto.accountKey
                            )
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


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]])
    def transferAllCreditCard(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList = dto.resourceKeyList))
            for creditCardResponseDto in creditCardResponseDtoList:
                for operation in dto.operationList:
                    self.service.security.shareResource(creditCardResponseDto.credit.key, 'Credit', operation, dto.accountKey, authorizationAccount)
                    self.service.security.shareResource(creditCardResponseDto.key, 'CreditCard', operation, dto.accountKey, authorizationAccount)
            if shareRelatedDomains:
                resourceKeyList = list(set([
                    purchaseResponseDto.key 
                    for innerCreditCardResponseDto in creditCardResponseDtoList
                    for purchaseResponseDto in self.getPurchases(innerCreditCardResponseDto)
                ]))
                if ObjectHelper.isNotEmpty(resourceKeyList):
                    self.transferAllPurchase(
                        [
                            AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                resourceKeyList = [*resourceKeyList],
                                domain = dto.domain,
                                operationList = [*dto.operationList],
                                accountKey = dto.accountKey
                            )
                        ],
                        shareRelatedDomains = False
                    )
            for creditCardResponseDto in creditCardResponseDtoList:
                for operation in dto.operationList:
                    self.service.security.revokeResourceAccess(creditCardResponseDto.credit.key, authorizationAccount.key, authorizationAccount)
                    self.service.security.revokeResourceAccess(creditCardResponseDto.key, authorizationAccount.key, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]])
    def transferAllPurchase(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            if ObjectHelper.isNotEmpty(dto.resourceKeyList):
                purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = dto.resourceKeyList))
                if shareRelatedDomains:
                    self.shareAllCreditCard(
                        [
                            AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                resourceKeyList = list(set([purchaseResponseDto.creditCardKey for purchaseResponseDto in purchaseResponseDtoList])),
                                domain = dto.domain,
                                operationList = dto.operationList,
                                accountKey = dto.accountKey
                            )
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
