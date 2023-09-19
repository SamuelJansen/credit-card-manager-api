from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod

from domain import ResourceDomain
from dto import AuthorizationAccessDto, CreditCardDto, PurchaseDto, InstallmentDto


def isValidShareOrTransferOperation(resourceKeyList, operationList):
    return ObjectHelper.isNotEmpty(resourceKeyList) and ObjectHelper.isNotEmpty(operationList)



@Service()
class ResourceService:


    @ServiceMethod(requestClass=[CreditCardDto.CreditCardResponseDto])
    def getPurchasesByCreditCardResponseDto(self, creditCardResponseDto):
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
                    self.service.security.shareResource(creditCardResponseDto.credit.key, ResourceDomain.CREDIT, operation, dto.accountKey, authorizationAccount)
                    self.service.security.shareResource(creditCardResponseDto.key, ResourceDomain.CREDIT_CARD, operation, dto.accountKey, authorizationAccount)
            if shareRelatedDomains:
                purchaseKeyList = list(set([
                    purchaseResponseDto.key 
                    for innerCreditCardResponseDto in creditCardResponseDtoList
                    for purchaseResponseDto in self.getPurchasesByCreditCardResponseDto(innerCreditCardResponseDto)
                    if ObjectHelper.isNotNone(purchaseResponseDto.key)
                ]))
                if isValidShareOrTransferOperation(purchaseKeyList, dto.operationList):
                    self.shareAllPurchase(
                        [
                            AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                resourceKeyList = [*purchaseKeyList],
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
            if isValidShareOrTransferOperation(dto.resourceKeyList, dto.operationList):
                purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = dto.resourceKeyList))
                if shareRelatedDomains:
                    creditCardKeyList = list(set([
                        purchaseResponseDto.creditCardKey 
                        for purchaseResponseDto in purchaseResponseDtoList
                        if ObjectHelper.isNotNone(purchaseResponseDto.creditCardKey)
                    ]))
                    if isValidShareOrTransferOperation(creditCardKeyList, dto.operationList):
                        self.shareAllCreditCard(
                            [
                                AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                    resourceKeyList = [*creditCardKeyList],
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
                            self.service.security.shareResource(installmentResponseDto.key, ResourceDomain.INSTALLMENT, operation, dto.accountKey, authorizationAccount)
                    for operation in dto.operationList:
                        self.service.security.shareResource(purchaseResponseDto.key, ResourceDomain.PURCHASE, operation, dto.accountKey, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)


    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]])
    def transferAllCreditCard(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList = dto.resourceKeyList))
            for creditCardResponseDto in creditCardResponseDtoList:
                for operation in dto.operationList:
                    self.service.security.shareResource(creditCardResponseDto.credit.key, ResourceDomain.CREDIT, operation, dto.accountKey, authorizationAccount)
                    self.service.security.shareResource(creditCardResponseDto.key, ResourceDomain.CREDIT_CARD, operation, dto.accountKey, authorizationAccount)
            if shareRelatedDomains:
                purchaseKeyList = list(set([
                    purchaseResponseDto.key 
                    for innerCreditCardResponseDto in creditCardResponseDtoList
                    for purchaseResponseDto in self.getPurchasesByCreditCardResponseDto(innerCreditCardResponseDto)
                    if ObjectHelper.isNotNone(purchaseResponseDto.key)
                ]))
                if isValidShareOrTransferOperation(purchaseKeyList, dto.operationList):
                    self.transferAllPurchase(
                        [
                            AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                resourceKeyList = [*purchaseKeyList],
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
            if isValidShareOrTransferOperation(dto.resourceKeyList, dto.operationList):
                purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = dto.resourceKeyList))
                if shareRelatedDomains:
                    creditCardKeyList = list(set([
                        purchaseResponseDto.creditCardKey 
                        for purchaseResponseDto in purchaseResponseDtoList
                        if ObjectHelper.isNotNone(purchaseResponseDto.creditCardKey)
                    ]))
                    if isValidShareOrTransferOperation(creditCardKeyList, dto.operationList):
                        self.shareAllCreditCard(
                            [
                                AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                    resourceKeyList = [*creditCardKeyList],
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
                            self.service.security.shareResource(installmentResponseDto.key, ResourceDomain.INSTALLMENT, operation, dto.accountKey, authorizationAccount)
                        self.service.security.revokeResourceAccess(installmentResponseDto.key, authorizationAccount.key, authorizationAccount)
                    for operation in dto.operationList:
                        self.service.security.shareResource(purchaseResponseDto.key, ResourceDomain.PURCHASE, operation, dto.accountKey, authorizationAccount)
                    self.service.security.revokeResourceAccess(purchaseResponseDto.key, authorizationAccount.key, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)

    
    @ServiceMethod(requestClass=[[AuthorizationAccessDto.AuthorizationAccessAllRequestDto]])
    def transferAllInstallment(self, dtoList, shareRelatedDomains=True):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            if isValidShareOrTransferOperation(dto.resourceKeyList, dto.operationList):
                installmentResponseDtoList = self.service.installment.findAllByQuery(InstallmentDto.InstallmentQueryAllDto(keyList = dto.resourceKeyList))
                installmentKeyList = list(set([
                    innerInstallmentResponseDto.key 
                    for innerInstallmentResponseDto in installmentResponseDtoList
                    if ObjectHelper.isNotNone(innerInstallmentResponseDto.key)
                ]))
                purchaseKeyList = list(set([
                    innerInstallmentResponseDto.purchaseKey 
                    for innerInstallmentResponseDto in installmentResponseDtoList
                    if ObjectHelper.isNotNone(innerInstallmentResponseDto.purchaseKey)
                ]))
                if isValidShareOrTransferOperation(installmentKeyList, dto.operationList) and isValidShareOrTransferOperation(purchaseKeyList, dto.operationList):
                    purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(keyList = purchaseKeyList))
                    if shareRelatedDomains:
                        creditCardKeyList = list(set([
                            purchaseResponseDto.creditCardKey 
                            for purchaseResponseDto in purchaseResponseDtoList
                            if ObjectHelper.isNotNone(purchaseResponseDto.creditCardKey)
                        ]))
                        if isValidShareOrTransferOperation(creditCardKeyList, dto.operationList):
                            self.shareAllCreditCard(
                                [
                                    AuthorizationAccessDto.AuthorizationAccessAllRequestDto(
                                        resourceKeyList = [*creditCardKeyList],
                                        domain = dto.domain,
                                        operationList = dto.operationList,
                                        accountKey = dto.accountKey
                                    )
                                ], 
                                shareRelatedDomains = False
                            )
                    for purchaseResponseDto in purchaseResponseDtoList:
                        foundPurchase = False
                        for installmentResponseDto in purchaseResponseDto.installmentList:
                            if installmentResponseDto.key in installmentKeyList:
                                foundPurchase = True
                                for operation in dto.operationList:
                                    self.service.security.shareResource(installmentResponseDto.key, ResourceDomain.INSTALLMENT, operation, dto.accountKey, authorizationAccount)
                                self.service.security.revokeResourceAccess(installmentResponseDto.key, authorizationAccount.key, authorizationAccount)
                        if foundPurchase:
                            for operation in dto.operationList:
                                self.service.security.shareResource(purchaseResponseDto.key, ResourceDomain.PURCHASE, operation, dto.accountKey, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)
