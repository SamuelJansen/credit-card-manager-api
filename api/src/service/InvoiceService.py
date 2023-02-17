from python_helper import ObjectHelper, DateTimeHelper
from python_framework import Service, ServiceMethod, Serializer, StaticConverter

from constant import InvoiceConstant
from helper.static import MathStaticHelper
from dto import InvoiceDto, InstallmentDto, CreditCardDto


@Service()
class InvoiceService:

    @ServiceMethod(requestClass=[InvoiceDto.InvoiceQueryDto])
    def findAllByQuery(self, queryDto):
        transactionKey = self.service.security.lockTransaction()
        creditCardResponseDtoList = self.service.creditCard.findAllByQuery(CreditCardDto.CreditCardQueryAllDto(keyList=[] if ObjectHelper.isEmpty(queryDto.creditCardKeyList) else queryDto.creditCardKeyList))
        invoiceResponseDtoList = []
        for creditCardResponseDto in creditCardResponseDtoList:
            dueDateTime = self.helper.invoice.getCurrentDueDateTime(DateTimeHelper.of(date=queryDto.date), creditCardResponseDto)
            dueDate = DateTimeHelper.dateOf(dateTime=dueDateTime)
            closingDateTime = self.helper.invoice.getCurrentClosingDateTime(DateTimeHelper.of(date=queryDto.date), creditCardResponseDto)
            closingDate = DateTimeHelper.dateOf(dateTime=closingDateTime)
            fromDateTimeRefference = closingDateTime if queryDto.date > dueDate else DateTimeHelper.minusMonths(closingDateTime, months=1)
            toDateTimeRefference = DateTimeHelper.plusMonths(fromDateTimeRefference, months=1)
            installmentResponseDtoList = self.service.installment.findAllByQuery(
                InstallmentDto.InstallmentQueryAllDto(
                    creditCardKeyList = [
                        creditCardResponseDto.key
                    ],
                    fromDateTime = f'{DateTimeHelper.dateOf(dateTime=DateTimeHelper.plusDays(fromDateTimeRefference, days=1))} {DateTimeHelper.DEFAULT_TIME_BEGIN}',
                    toDateTime = f'{DateTimeHelper.dateOf(dateTime=toDateTimeRefference)} {DateTimeHelper.DEFAULT_TIME_END}'
                )
            )
            toYearMonthList = f'{DateTimeHelper.dateOf(dateTime=toDateTimeRefference)}'.split('-')[:-1]
            closeAt = f'{toYearMonthList[0]}-{toYearMonthList[1]}-{creditCardResponseDto.closingDay:02}'
            dueAt = f'{toYearMonthList[0]}-{toYearMonthList[1]}-{creditCardResponseDto.dueDay:02}'
            invoiceResponseDtoList.append(
                InvoiceDto.InvoiceResponseDto(
                    key = creditCardResponseDto.key,
                    value = MathStaticHelper.sumIt(
                        [
                            installmentResponseDto.value
                            for installmentResponseDto in installmentResponseDtoList
                            if (
                                installmentResponseDto.value < 0  and
                                installmentResponseDto.status in InvoiceConstant.INSTALLMENT_COUNTABLE_TYPES
                            )
                        ]
                    ),
                    installmentList = sorted(installmentResponseDtoList, key=lambda x: x.installmentAt, reverse=True),
                    creditCard = creditCardResponseDto,
                    closeAt = closeAt,
                    dueAt = dueAt
                )
            )
        self.service.security.unlockTransaction(transactionKey)
        return invoiceResponseDtoList
