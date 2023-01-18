from python_helper import ObjectHelper, DateTimeHelper
from python_framework import Service, ServiceMethod, Serializer, StaticConverter

from constant import InvoiceConstant
from helper.static import MathStaticHelper
from dto import InvoiceDto, InstallmentDto, CreditCardDto


@Service()
class InvoiceService:

    @ServiceMethod(requestClass=[InvoiceDto.InvoiceQueryDto])
    def findAllByQuery(self, queryDto):
        creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList=[] if ObjectHelper.isEmpty(queryDto.keyList) else queryDto.keyList))
        invoiceResponseDtoList = []
        for creditCardResponseDto in creditCardResponseDtoList:
            closingDateTime = self.helper.installment.getCurrentClosingDateTime(DateTimeHelper.of(date=queryDto.date), creditCardResponseDto)
            closingDate = DateTimeHelper.dateOf(dateTime=closingDateTime)
            fromDateTime = closingDateTime if queryDto.date >= closingDate else DateTimeHelper.minusMonths(closingDateTime, months=1)
            toDateTime = closingDateTime if queryDto.date < closingDate else DateTimeHelper.plusMonths(closingDateTime, months=1)
            installmentResponseDtoList = self.service.installment.findAllByQuery(
                InstallmentDto.InstallmentQueryAllDto(
                    creditCardKeyList = [
                        creditCardResponseDto.key
                    ],
                    fromDateTime = f'{DateTimeHelper.dateOf(dateTime=fromDateTime)} {DateTimeHelper.DEFAULT_TIME_BEGIN}',
                    toDateTime = f'{DateTimeHelper.dateOf(dateTime=toDateTime)} {DateTimeHelper.DEFAULT_TIME_END}'
                )
            )
            toYearMonthList = f'{DateTimeHelper.dateOf(dateTime = toDateTime)}'.split('-')[:-1]
            closeAt = f'{toYearMonthList[0]}-{toYearMonthList[1]}-{creditCardResponseDto.closingDay:02}'
            dueAt = f'{toYearMonthList[0]}-{toYearMonthList[1]}-{creditCardResponseDto.dueDay:02}'
            invoiceResponseDtoList.append(
                InvoiceDto.InvoiceResponseDto(
                    key = creditCardResponseDto.key,
                    value = MathStaticHelper.roundIt(
                        sum(
                            [
                                installmentResponseDto.value
                                for installmentResponseDto in installmentResponseDtoList
                                if installmentResponseDto.status in InvoiceConstant.INSTALLMENT_COUNTABLE_TYPES
                            ]
                        )
                    ),
                    installmentList = sorted(installmentResponseDtoList, key=lambda x: x.installmentAt, reverse=True), ###- ut.sort(key=lambda x: x.count, reverse=True)
                    creditCard = creditCardResponseDto,
                    closeAt = closeAt,
                    dueAt = dueAt
                )
            )
        return invoiceResponseDtoList
