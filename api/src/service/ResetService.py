from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, Serializer, HttpStatus, GlobalException

from dto import ResetDto, PurchaseDto

from dto import CreditDto, CreditCardDto



def buildCreditRequestFromFirstCreditResponse(creditkey, creditCardDtoList):
    for creditCardDto in creditCardDtoList:
        if ObjectHelper.equals(creditCardDto.creditKey, creditkey):
            return CreditDto.CreditRequestDto(
                key = creditCardDto.credit.key,
                limit = creditCardDto.credit.limit,
                customLimit = creditCardDto.credit.customLimit,
                value = 0.0
            )



def buildCreditCardRequestFromFirstCreditCardResponse(creditCardkey, creditCardDtoList):
    for creditCardDto in creditCardDtoList:
        if ObjectHelper.equals(creditCardDto.key, creditCardkey):
            return CreditCardDto.CreditCardRequestDto(
                key = creditCardDto.key,
                creditKey = creditCardDto.creditKey,
                label = creditCardDto.label,
                customLimit = creditCardDto.customLimit,
                value = 0.0,
                expirationDate = creditCardDto.expirationDate,
                closingDay = creditCardDto.closingDay,
                dueDay = creditCardDto.dueDay
            )



@Service()
class ResetService:

    @ServiceMethod(requestClass=[[ResetDto.ResetRequestDto]])
    def resetAll(self, dtoList):
        if ObjectHelper.isEmpty(dtoList):
            creditCardDtoList = self.service.creditCard.findAll()
            distinctCreditKeyList = list(set([
                creditCardDto.creditKey
                for creditCardDto in creditCardDtoList
            ]))
            return self.resetAll([
                ResetDto.ResetRequestDto(
                    credit = buildCreditRequestFromFirstCreditResponse(creditkey, creditCardDtoList),
                    creditCardList = [
                        buildCreditCardRequestFromFirstCreditCardResponse(creditCardkey, creditCardDtoList)
                        for creditCardkey in list(set([
                            creditCardDto.key
                            for creditCardDto in creditCardDtoList
                            if ObjectHelper.equals(creditCardDto.creditKey, creditkey)
                        ]))
                    ]
                )
                for creditkey in distinctCreditKeyList
            ])
        return [
            self.reset(dto)
            for dto in dtoList
        ]


    @ServiceMethod(requestClass=[ResetDto.ResetRequestDto])
    def reset(self, dto):     
        creditDto = self.service.credit.findByKey(dto.credit.key)
        creditCardDtoList = self.service.creditCard.findAllByKeyIn([
                creditCardDto.key
                for creditCardDto in dto.creditCardList
        ])
        creditCardKeyList = [
            creditCardDto.key
            for creditCardDto in creditCardDtoList
        ]
        purchaseDtoList = self.service.purchase.findAllByQuery(
            PurchaseDto.PurchaseQueryAllDto(
                creditCardKeyList = creditCardKeyList
            )
        )
        purchaseKeyList = [
            purchaseDto.key 
            for purchaseDto in purchaseDtoList
        ]
        installmentKeyList = [
            installmentDto.key
            for installmentDto in ObjectHelper.flatMap([
                purchaseDto.installmentList
                for purchaseDto in purchaseDtoList
            ])  
        ]
        if ObjectHelper.isNotEmpty(installmentKeyList):
            self.service.installment.deleteAllByKeyIn(installmentKeyList)
        if ObjectHelper.isNotEmpty(purchaseKeyList):
            self.service.purchase.deleteAllByKeyIn(purchaseKeyList)
        
        self.service.creditCard.deleteAllByKeyIn(creditCardKeyList)
        self.service.credit.deleteByKey(creditDto.key)
        newCredit = self.service.credit.create(dto.credit)
        newCreditCardList = self.service.creditCard.createAll(dto.creditCardList)
        return ResetDto.ResetResponseDto(
            credit = newCredit,
            creditCardList = newCreditCardList
        )
        
        
