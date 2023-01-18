from python_framework import Mapper, MapperMethod

from model import Purchase
from dto import PurchaseDto, CreditCardDto, InstallmentDto

@Mapper()
class PurchaseMapper:

    @MapperMethod(requestClass=[[PurchaseDto.PurchaseRequestDto]], responseClass=[[Purchase.Purchase]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList

    @MapperMethod(requestClass=[[Purchase.Purchase]], responseClass=[[PurchaseDto.PurchaseResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList

    @MapperMethod(requestClass=[PurchaseDto.PurchaseRequestDto], responseClass=[Purchase.Purchase])
    def fromRequestDtoToModel(self, dto, model):
        return model

    @MapperMethod(requestClass=[Purchase.Purchase], responseClass=[PurchaseDto.PurchaseResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto

    @MapperMethod(requestClass=[[Purchase.Purchase], [CreditCardDto.CreditCardResponseDto], [InstallmentDto.InstallmentResponseDto]])
    def toResponseDtoList(self, modelList, creditCardResponseDtoList, installmentResponseDtoList):
        responseDtoList = self.fromModelListToResponseDtoList(modelList)
        self.converter.purchase.overrideResponseDtoList(responseDtoList, creditCardResponseDtoList, installmentResponseDtoList)
        return responseDtoList

    @MapperMethod(requestClass=[Purchase.Purchase, CreditCardDto.CreditCardResponseDto, [InstallmentDto.InstallmentResponseDto]])
    def toResponseDto(self, model, creditCardResponseDto, installmentResponseDtoList):
        responseDto = self.fromModelToResponseDto(model)
        self.converter.purchase.overrideResponseDto(responseDto, creditCardResponseDto, installmentResponseDtoList)
        return responseDto
