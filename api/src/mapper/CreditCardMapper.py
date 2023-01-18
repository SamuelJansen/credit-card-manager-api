from python_framework import Mapper, MapperMethod

from model import CreditCard
from dto import CreditCardDto, CreditDto

@Mapper()
class CreditCardMapper:

    @MapperMethod(requestClass=[[CreditCardDto.CreditCardRequestDto]], responseClass=[[CreditCard.CreditCard]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList

    @MapperMethod(requestClass=[[CreditCard.CreditCard]], responseClass=[[CreditCardDto.CreditCardResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList

    @MapperMethod(requestClass=[CreditCardDto.CreditCardRequestDto], responseClass=[CreditCard.CreditCard])
    def fromRequestDtoToModel(self, dto, model):
        return model

    @MapperMethod(requestClass=[CreditCard.CreditCard], responseClass=[CreditCardDto.CreditCardResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto

    @MapperMethod(requestClass=[[CreditCard.CreditCard], [CreditDto.CreditResponseDto]])
    def toResponseDtoList(self, modelList, creditResponseDtoList):
        responseDtoList = self.fromModelListToResponseDtoList(modelList)
        self.converter.creditCard.overrideResponseDtoList(responseDtoList, creditResponseDtoList)
        return responseDtoList

    @MapperMethod(requestClass=[CreditCard.CreditCard, CreditDto.CreditResponseDto])
    def toResponseDto(self, model, creditResponseDto):
        responseDto = self.fromModelToResponseDto(model)
        self.converter.creditCard.overrideResponseDto(responseDto, creditResponseDto)
        return responseDto
