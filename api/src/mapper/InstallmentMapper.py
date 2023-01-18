from python_helper import DateTimeHelper
from python_framework import Mapper, MapperMethod, EnumItem

from enumeration.InstallmentStatus import InstallmentStatus
from model import Installment
from dto import InstallmentDto, PurchaseDto

@Mapper()
class InstallmentMapper:

    @MapperMethod(requestClass=[[InstallmentDto.InstallmentRequestDto]], responseClass=[[Installment.Installment]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList

    @MapperMethod(requestClass=[[Installment.Installment]], responseClass=[[InstallmentDto.InstallmentResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList

    @MapperMethod(requestClass=[InstallmentDto.InstallmentRequestDto], responseClass=[Installment.Installment])
    def fromRequestDtoToModel(self, dto, model):
        return model

    @MapperMethod(requestClass=[Installment.Installment], responseClass=[InstallmentDto.InstallmentResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto

    @MapperMethod(requestClass=[[Installment.Installment], [PurchaseDto.PurchaseResponseDto]])
    def toResponseDtoList(self, modelList, purchaseResponseDtoList):
        responseDtoList = self.fromModelListToResponseDtoList(modelList)
        self.converter.installment.overrideResponseDtoList(responseDtoList, purchaseResponseDtoList)
        return responseDtoList

    @MapperMethod(requestClass=[Installment.Installment, PurchaseDto.PurchaseResponseDto])
    def toResponseDto(self, model, purchaseResponseDto):
        responseDto = self.fromModelToResponseDto(model)
        self.converter.installment.overrideResponseDto(responseDto, purchaseResponseDto)
        return responseDto

    @MapperMethod(requestClass=[InstallmentDto.InstallmentRequestDto], responseClass=[Installment.Installment])
    def buildNewScheaduledModel(self, dto, model):
        return self.overrideModelStatus(
            model,
            InstallmentStatus.SCHEADULED if model.installmentAt > DateTimeHelper.now() else InstallmentStatus.PROCESSING
        )

    @MapperMethod(requestClass=[[InstallmentDto.InstallmentRequestDto]])
    def buildNewScheaduledModelList(self, dtoList):
        return [
            self.buildNewScheaduledModel(dto)
            for dto in dtoList
        ]

    @MapperMethod(requestClass=[InstallmentDto.InstallmentRequestDto], responseClass=[Installment.Installment])
    def buildNewCreatedModel(self, dto, model):
        return self.overrideModelStatus(model, InstallmentStatus.CREATED)

    @MapperMethod(requestClass=[[InstallmentDto.InstallmentRequestDto]])
    def buildNewCreatedModelList(self, dtoList):
        return [
            self.buildNewCreatedModel(dto)
            for dto in dtoList
        ]

    @MapperMethod(requestClass=[[Installment.Installment], EnumItem])
    def overrideModelListStatus(self, modelList, status):
        return [
            self.overrideModelStatus(model, status)
            for model in modelList
        ]

    @MapperMethod(requestClass=[Installment.Installment, EnumItem])
    def overrideModelStatus(self, model, status):
        model.status = status
        return model
