from python_framework import Converter, ConverterMethod

from constant import InstallmentConstant
from dto import InstallmentDto, PurchaseDto

@Converter()
class InstallmentConverter:

    @ConverterMethod(requestClass=[[InstallmentDto.InstallmentResponseDto], [PurchaseDto.PurchaseResponseDto]])
    def overrideResponseDtoList(self, dtoList, purchaseResponseDtoList):
        return [
            self.overrideResponseDto(
                dto,
                [
                    purchaseResponseDto
                    for purchaseResponseDto in purchaseResponseDtoList
                    if dto.purchaseKey == purchaseResponseDto.key
                ][-1],
            )
            for dto in dtoList
        ]

    @ConverterMethod(requestClass=[InstallmentDto.InstallmentResponseDto, PurchaseDto.PurchaseResponseDto])
    def overrideResponseDto(self, dto, purchaseResponseDto):
        dto.purchase = purchaseResponseDto
        return dto

    @ConverterMethod(requestClass=[InstallmentDto.InstallmentQueryAllDto])
    def overrideProcessableQueryDto(self, queryDto):
        queryDto.statusList = [
            *InstallmentConstant.PROCCESSABLE_STATUS
        ]
