from python_framework import Converter, ConverterMethod

from dto import CreditCardDto, CreditDto

@Converter()
class CreditCardConverter:

    @ConverterMethod(requestClass=[[CreditCardDto.CreditCardResponseDto], [CreditDto.CreditResponseDto]])
    def overrideResponseDtoList(self, dtoList, creditResponseDtoList):
        return [
            self.overrideResponseDto(dto, creditDto)
            for dto in dtoList
            for creditDto in creditResponseDtoList
            if dto.creditKey == creditDto.key
        ]

    @ConverterMethod(requestClass=[CreditCardDto.CreditCardResponseDto, CreditDto.CreditResponseDto])
    def overrideResponseDto(self, dto, creditDto):
        dto.credit = creditDto
        return dto
