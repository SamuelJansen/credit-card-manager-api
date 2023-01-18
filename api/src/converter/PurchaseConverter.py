from python_framework import Converter, ConverterMethod

from dto import PurchaseDto, CreditCardDto, InstallmentDto

@Converter()
class PurchaseConverter:

    @ConverterMethod(requestClass=[[PurchaseDto.PurchaseResponseDto], [CreditCardDto.CreditCardResponseDto], [InstallmentDto.InstallmentResponseDto]])
    def overrideResponseDtoList(self, dtoList, creditCardResponseDtoList, installmentResponseDtoList):
        return [
            self.overrideResponseDto(
                dto,
                [
                    creditCardResponseDto
                    for creditCardResponseDto in creditCardResponseDtoList
                    if dto.creditCardKey == creditCardResponseDto.key
                ][-1],
                [
                    instalmentResponseDto
                    for instalmentResponseDto in installmentResponseDtoList
                    if dto.key == instalmentResponseDto.purchaseKey
                ]
            )
            for dto in dtoList
        ]

    @ConverterMethod(requestClass=[PurchaseDto.PurchaseResponseDto, CreditCardDto.CreditCardResponseDto, [InstallmentDto.InstallmentResponseDto]])
    def overrideResponseDto(self, dto, creditCardResponseDto, installmentResponseDtoList):
        dto.creditCard = creditCardResponseDto
        dto.installmentList = installmentResponseDtoList
        return dto
