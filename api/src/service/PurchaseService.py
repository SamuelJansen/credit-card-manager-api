from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod, Serializer, HttpStatus, GlobalException

from AuthorizedServiceMethodAnnotation import AuthorizedServiceMethod

from domain import AuthorizationOperation
from dto import PurchaseDto, InstallmentDto
from model import Purchase
from helper.static import MathStaticHelper


@Service()
class PurchaseService:

    @ServiceMethod(requestClass=[[str]])
    def findAllByKeyIn(self, keyList):
        modelList = self.findAllModelByQuery(
            PurchaseDto.PurchaseQueryAllDto(
                keyList = keyList
            )
        )
        return self.mapper.purchase.fromModelListToResponseDtoList(modelList)


    @ServiceMethod(requestClass=[PurchaseDto.PurchaseQueryAllDto])
    def findAllByQuery(self, queryDto):
        modelList = self.findAllModelByQuery(queryDto)
        creditCardDtoList = self.service.creditCard.findAllByKeyIn([
            model.creditCardKey
            for model in modelList
        ])
        installmentResponseDtoList = self.service.installment.findAllByPurchaseKeyIn(
            [
                model.key
                for model in modelList
                if ObjectHelper.isNotNone(model.key)
            ]
        )
        return self.mapper.purchase.toResponseDtoList(modelList, creditCardDtoList, installmentResponseDtoList)


    @AuthorizedServiceMethod(requestClass=[PurchaseDto.PurchaseQueryAllDto], operations=[AuthorizationOperation.GET])
    def findAllModelByQuery(self, queryDto, authorizedRequest):
        if ObjectHelper.isEmpty(queryDto.keyList):
            for resourceKey in authorizedRequest.resourceKeys:
                if resourceKey not in queryDto.keyList:
                    queryDto.keyList.append(resourceKey)
        query = Serializer.getObjectAsDictionary(queryDto)
        return self.repository.purchase.findAllByQuery(query)


    @AuthorizedServiceMethod(requestClass=[[PurchaseDto.PurchaseRequestDto]], operations=[AuthorizationOperation.POST])
    def createAll(self, dtoList, authorizedRequest):
        return [
            self.create(dto)
            for dto in dtoList
        ]


    @AuthorizedServiceMethod(requestClass=[PurchaseDto.PurchaseRequestDto], operations=[AuthorizationOperation.POST])
    def create(self, dto, authorizedRequest):
        creditCardResponseDto = self.service.creditCard.findByKey(dto.creditCardKey)
        if creditCardResponseDto.credit.customLimit - creditCardResponseDto.credit.value > dto.value:
            raise GlobalException(message='Not enought funds', status=HttpStatus.BAD_REQUEST)
        model = self.mapper.purchase.fromRequestDtoToModel(dto)
        self.saveAllModel([model])
        responseDto = self.mapper.purchase.fromModelToResponseDto(model)
        installmentValue = MathStaticHelper.roundIt(responseDto.value / responseDto.installments)
        installmentResponseDtoList = self.service.installment.newCreatedAll(
            [
                InstallmentDto.InstallmentRequestDto(
                    purchaseKey = responseDto.key,
                    label = f'{responseDto.label}',
                    value = installmentValue if nthInstallment > 0 else installmentValue + MathStaticHelper.roundIt(
                        responseDto.value - installmentValue * responseDto.installments
                    ),
                    installmentAt = self.helper.installment.getInstallmentAt(responseDto, creditCardResponseDto, nthInstallment),
                    installments = responseDto.installments,
                    order = nthInstallment
                )
                for nthInstallment in range(responseDto.installments)
            ]
        )
        return self.mapper.purchase.toResponseDto(model, creditCardResponseDto, installmentResponseDtoList)


    @ServiceMethod(requestClass=[[Purchase.Purchase]])
    def saveAllModel(self, modelList):
        return self.repository.purchase.saveAll(modelList)


    @AuthorizedServiceMethod(requestClass=[str], operations=[AuthorizationOperation.DELETE])
    def deleteByKey(self, key, authorizedRequest):
        self.repository.purchase.deleteByKey(key)
