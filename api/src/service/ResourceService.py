from python_framework import Service, ServiceMethod

from dto import AuthorizationAccessShareDto, CreditCardDto, PurchaseDto


@Service()
class ResourceService:


    @ServiceMethod(requestClass=[[AuthorizationAccessShareDto.AuthorizationAccessShareRequestDto]])
    def shareAllCreditCard(self, dtoList):
        transactionKey = self.service.security.lockTransaction()
        authorizationAccount = self.service.security.getAuthorizationAccount()
        for dto in dtoList:
            creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList = [dto.resourceKey]))
            for creditCardResponseDto in creditCardResponseDtoList:
                self.service.security.shareResource(creditCardResponseDto.credit.key, 'Credit', dto.operation, dto.accountKey, authorizationAccount)
                self.service.security.shareResource(creditCardResponseDto.key, 'CreditCard', dto.operation, dto.accountKey, authorizationAccount)
                purchaseResponseDtoList = self.service.purchase.findAllByQuery(PurchaseDto.PurchaseQueryAllDto(creditCardKeyList = [creditCardResponseDto.key]))
                for purchaseResponseDto in purchaseResponseDtoList:
                    for installmentResponseDto in purchaseResponseDto.installmentList:
                        self.service.security.shareResource(installmentResponseDto.key, 'Installment', dto.operation, dto.accountKey, authorizationAccount)
                    self.service.security.shareResource(purchaseResponseDto.key, 'Purchase', dto.operation, dto.accountKey, authorizationAccount)
        self.service.security.unlockTransaction(transactionKey)
