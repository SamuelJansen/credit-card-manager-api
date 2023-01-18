from python_framework import Mapper, MapperMethod

from model import Credit
from dto import CreditDto

@Mapper()
class CreditMapper:

    @MapperMethod(requestClass=[[CreditDto.CreditRequestDto]], responseClass=[[Credit.Credit]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList

    @MapperMethod(requestClass=[[Credit.Credit]], responseClass=[[CreditDto.CreditResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList

    @MapperMethod(requestClass=[CreditDto.CreditRequestDto], responseClass=[Credit.Credit])
    def fromRequestDtoToModel(self, dto, model):
        return model

    @MapperMethod(requestClass=[Credit.Credit], responseClass=[CreditDto.CreditResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto
